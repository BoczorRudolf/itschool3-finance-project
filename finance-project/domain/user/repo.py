import logging
import uuid

from domain.exceptions import UserIdNotFound, UserIDNotFound
from singleton import singleton

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)




@singleton
class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        logging.debug("Initialize UserRepo")
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        try:
            if self.__users is None:
                self.__users = self.__persistence.get_all()
            self.__persistence.add(new_user)
            self.__users.append(new_user)
            logging.info(
                f"The user with username '{new_user.username}' was created, having the id '{new_user.id}'."
            )
        except Exception as e:
            logging.error(f"Failed to add user: {e}")
            raise e

    def get_all(self) -> list[User]:
        try:
            if self.__users is None:
                self.__users = self.__persistence.get_all()
            return self.__users
        except Exception as e:
            logging.error(f"Failed to get all users: {e}")
            raise e

    def get_by_id(self, uid: str) -> User:
        try:
            if self.__users is None:
                self.__users = self.__persistence.get_all()
            for user in self.__users:
                if user.id == uuid.UUID(hex=uid):
                    assets = AssetRepo().get_for_user(user)
                    return User(
                        uuid=user.id,
                        username=user.username,
                        stocks=assets
                    )
            raise UserIdNotFound("This user's id was not found.")
        except Exception as e:
            logging.error(f"Failed to get user by id: {e}")
            raise e

    def delete(self, uid: str):
        try:
            self.__check_we_have_users()
            self.__persistence.delete(uid)
            for user in self.__users:
                if user.id == uuid.UUID(hex=uid):
                    self.__users.remove(user)
                    logging.info(f"The user with the id {uid} was deleted.")
                    break
            else:
                raise UserIdNotFound("This user's id was not found.")
        except Exception as e:
            logging.error(f"Failed to delete user: {e}")
            raise e

    def update(self, user_id: str, username: str):
        try:
            self.__check_we_have_users()
            if user_id not in [str(u.id) for u in self.__users]:
                raise UserIdNotFound("This user's id was not found.")
            self.__persistence.update(user_id, username)
            for user in self.__users:
                if user.id == uuid.UUID(hex=user_id):
                    user.username = username
            logging.info(f"The user with the id {user_id} has been replaced with {username}.")
        except Exception as e:
            logging.error(f"Failed to update user: {e}")
            raise e

    def __check_we_have_users(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()

    def __check_id_exists(self, user_id):
        if str(user_id) not in [str(user.id) for user in self.__users]:
            error_message = "The specified user ID does not exist."
            logging.error(msg=error_message)
            raise UserIDNotFound(error_message)
