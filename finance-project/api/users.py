import json
import logging

from fastapi import APIRouter, Depends

from config.asset_config import check_asset_persistence_type
from config.config import persistence_type_by_choosing
from domain.asset.factory import AssetFactory
from domain.asset.repo import AssetRepo
from domain.exceptions import EntityNotFoundException
from domain.user.factory import UserFactory
from domain.user.repo import UserRepo
from api.models import UserAdd, UserInfo, AssetInfoUser, AssetAdd


users_router = APIRouter(prefix="/users")


def get_asset_repo() -> AssetRepo:
    asset_persistence = check_asset_persistence_type("config/config.json")
    return AssetRepo(asset_persistence)


def get_user_repo() -> UserRepo:
    user_persistence = persistence_type_by_choosing("config/config.json")
    asset_persistence = check_asset_persistence_type("config/config.json")
    return UserRepo(user_persistence, asset_persistence)


@users_router.get("", response_model=list[UserInfo])
def get_all_users(repo=Depends(get_user_repo)):
    return repo.get_all()


@users_router.get("/{user_id}", response_model=UserInfo)
def get_user_by_id(user_id: str, repo=Depends(get_user_repo)):
    return repo.get_by_id(user_id)


@users_router.delete("/{user_id}")
def delete_user(user_id: str, repo=Depends(get_user_repo)):
    try:
        repo.delete_by_id(user_id)

        logging.info(f"User {user_id} deleted successfully")
        return {"message": "User deleted successfully"}
    except EntityNotFoundException as e:
        logging.warning(f"User {user_id} not found: {str(e)}")
        return {"message": "User not found"}
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {str(e)}")
        return {"message": "User not found"}


@users_router.post("", response_model=UserInfo)
def create_a_user(new_user: UserAdd, repo=Depends(get_user_repo)):
    user = UserFactory().make_new(new_user.username)
    repo.add(user)
    return user


@users_router.put("/{user_id}", response_model=UserInfo)
def edit_by_id(user_id: str, username: str, repo=Depends(get_user_repo)):
    repo.edit(user_id, username)
    return repo.get_by_id(user_id)


@users_router.post("/{user_id}/assets", response_model=AssetInfoUser)
def add_asset_to_user(
    user_id: str,
    asset: AssetAdd,
    repo=Depends(get_user_repo),
    asset_repo=Depends(get_asset_repo),
):
    new_asset = AssetFactory().make_new(asset.ticker)
    user = repo.get_by_id(user_id)
    asset_repo.add(user, new_asset)

    return new_asset
