import json
import logging

from fastapi import APIRouter, Depends
from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.exceptions import InvalidPersistenceType, EntityNotFoundException
from domain.user.factory import UserFactory
from domain.user.repo import UserRepo
from api.models import UserAdd, UserInfo, AssetInfoUser, AssetAdd
from persistence.user_file import UserPersistenceFile
from persistence.user_sqlite import UserPersistenceSqlite

users_router = APIRouter(prefix="/users")

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)

def check_persistence(file_path):
    with open(file_path, 'r') as choose_config:
        persistence_type = choose_config.read()
        data = json.loads(persistence_type)
        if "sqlite" in str(data["persistence_type"]):
            return UserPersistenceSqlite()
        elif "json" in str(data["persistence_type"]):
            return UserPersistenceFile("main_users.json")
        else:
            raise InvalidPersistenceType("Unrecognized persistence config type. Please check config.json file.")

def get_user_repo() -> UserRepo:
    try:
        user_persistence = check_persistence("configuration/config.json")
    except InvalidPersistenceType as e:
        logging.exception(f"Failed to load user repository: {e}")
        raise
    return UserRepo(user_persistence)

@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all()

@users_router.get("/{user_id}", response_model=UserInfo)
def get_user(user_id: str, repo=Depends(get_user_repo)):
    try:
        user = repo.get_by_id(user_id)
    except ValueError as e:
        logging.exception(f"Failed to get user with ID {user_id}: {e}")
        raise
    return user

@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    user = UserFactory().make_new(new_user.username)
    try:
        repo.add(user)
    except ValueError as e:
        logging.exception(f"Failed to create user {new_user.username}: {e}")
        raise
    return user

@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(user_id: str,  asset: AssetAdd, repo=Depends(get_user_repo)):
    new_asset = AssetFactory().make_new(asset.ticker)
    try:
        user = repo.get_by_id(user_id)
    except ValueError as e:
        logging.exception(f"Failed to add asset to user with ID {user_id}: {e}")
        raise
    try:
        user.add_stock(new_asset)
        AssetRepo().add_to_user(user, new_asset)
    except ValueError as e:
        logging.exception(f"Failed to add asset {new_asset.ticker} to user {user.username}: {e}")
        raise
    return new_asset

@users_router.put("/{user_id}", response_model=UserInfo)
def update_user(user_id: str, username: str, repo=Depends(get_user_repo)):
    try:
        repo.update(user_id, username)
    except ValueError as e:
        logging.exception(f"Failed to update user with ID {user_id}: {e}")
        raise
    return repo.get_by_id(user_id)





@users_router.delete("/{user_id}")
def delete_user(user_id: str, repo=Depends(get_user_repo)):
    try:
        repo.delete(user_id)
        logging.info(f"User {user_id} deleted successfully")
        return {"message": "User deleted successfully"}
    except EntityNotFoundException as e:
        logging.warning(f"User {user_id} not found: {str(e)}")
        return {"message": "User not found"}
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return {"message": "Error deleting user"}