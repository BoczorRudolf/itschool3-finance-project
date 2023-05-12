import logging
import uuid
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateUser
from domain.user.persistance_interface import UserPersistenceInterface
from singleton import singleton

from domain.user.user import User


class UserNotFound(Exception):
    pass


class InvalidUID(Exception):
    pass


@singleton
class UserRepo:
    def __init__(
        self, persistence: UserPersistenceInterface, asset: AssetPersistenceInterface
    ):
        print("Init user repo")
        self.__persistence = persistence
        self.__users = None
        self.__asset = asset

    def add(self, new_user: User):
        logging.info("UserRepo executing add command...")
        self.__check_we_have_users()
        self.__persistence.add(new_user)
        self.__users.append(new_user)
        logging.info("UserRepo add command was successfully executed")

    def get_all(self) -> list[User]:
        logging.info("UserRepo executing get all command...")
        self.__check_we_have_users()
        return self.__users

    def get_by_id(self, uid: str) -> User:
        try:
            uuid_obj = uuid.UUID(hex=uid)
        except ValueError as e:
            raise InvalidUID(f"Invalid UID format: {uid}") from e

        logging.info("UserRepo executing get by id command...")
        self.__check_we_have_users()

        for u in self.__users:
            if u.id == uuid_obj:
                assets = self.__asset.get_for_user(u)
                logging.info("UserRepo get by id command was successfully executed")
                return User(
                    uuid=u.id,
                    username=u.username,
                    stocks=assets,
                )

        raise UserNotFound(f"User with UID {uid} not found")

    def delete_by_id(self, uid: str):
        logging.info("UserRepo executing delete command...")
        try:
            self.__persistence.delete_by_id(uid)
            logging.info("UserRepo delete command was successfully executed")
        except ValueError as e:
            logging.error(f"UserRepo delete by id command failed with error: {e}")
            raise (f"User deletion failed with error: {e}")

    def edit(self, user_id: str, username: str):
        logging.info("UserRepo executing update command...")
        self.__check_we_have_users()
        self.__persistence.edit(user_id, username)
        for user in self.__users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = username
        logging.info("UserRepo update command was successfully executed")

    def __check_we_have_users(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()
