import json
import logging
import uuid
import os

from domain.asset.repo import AssetRepo
from domain.exceptions import FileError
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface

from domain.user.user import User

logging.basicConfig(
    filename="finance.log",
    level=logging.DEBUG,
    format="%(asctime)s _ %(levelname)s _ %(name)s _ %(message)s",
)


class UserPersistenceFile(UserPersistenceInterface):
    def __init__(self, file_path: str):
        self.__file_path = file_path

    def read_file(self):
        try:
            with open(self.__file_path) as file:
                contents = file.read()
                users_info = json.loads(contents)
                factory = UserFactory()
                return [factory.make_from_persistence(x) for x in users_info]
        except FileNotFoundError:
            return []
        except Exception as e:
            raise FileError(f"Error reading file: {e}")

    def write_file(self, current_users):
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as file:
                file.write(users_json)
        except Exception as e:
            raise FileError(f"Error writing to file: {e}")

    def get_all(self) -> list[User]:
        try:
            current_users = self.read_file()
            return current_users
        except FileError as e:
            logging.warning(f"Could not get all users, will return empty list. Reason: {e}")
            return []

    def add(self, user: User):
        current_users = self.read_file()
        current_users.append(user)
        try:
            self.write_file(current_users)
        except FileError as e:
            logging.error(f"Could not add user to file. Error: {e}")

    def delete(self, uid: str):
        current_users = self.read_file()
        updated_users_list = [u for u in current_users if u.id != uuid.UUID(hex=uid)]
        try:
            self.write_file(updated_users_list)
        except FileError as e:
            logging.error(f"Could not delete user from file. Error: {e}")

    def update(self, user_id: str, new_username: str):
        current_users = self.read_file()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = new_username
                break
        try:
            self.write_file(current_users)
        except FileError as e:
            logging.error(f"Could not update file. Error: {e}")
