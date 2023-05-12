import json
import uuid
import logging

from config.asset_config import check_asset_persistence_type
from domain.exceptions import FailToWriteToFile, ErrorWhenWritingInPersistence
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

    def get_all(self) -> list[User]:
        try:
            with open(self.__file_path) as f:
                contents = f.read()
            users_info = json.loads(contents)
            factory = UserFactory()
            return [factory.make_from_persistence(x) for x in users_info]

        except Exception as e:
            logging.error(f"Could not read file {self.__file_path}, reason: {str(e)}")
            return []

    def add(self, user: User):
        logging.info("UserPersistenceFile executing add command...")
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info, indent=4)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
                logging.info(
                    f"UserPersistenceFile add command successfully executed, added {user.username} to file"
                )
        except FailToWriteToFile as e:
            logging.error("Could not write file. Error: " + str(e))
            raise e

    def get_by_id(self, uid: str) -> User:
        try:
            current_users = self.get_all()

            asset_persistence = check_asset_persistence_type("config.json")
            for u in current_users:
                if u.id == uuid.UUID(hex=uid):
                    assets = asset_persistence.get_all(u)

                    return User(uuid=u.id, username=u.username, stocks=assets)
            raise ValueError(f"No user with ID {uid} found.")
        except Exception as e:
            logging.error(f"Failed to get user with ID {uid}: {str(e)}")
            raise e

    def delete_by_id(self, uid: str):
        current_users = self.get_all()
        users_without_id = [u for u in current_users if u.id != uuid.UUID(hex=uid)]
        users_info = [(str(x.id), x.username, x.stocks) for x in users_without_id]
        json_current_users = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as f:
                f.write(json_current_users)
        except ErrorWhenWritingInPersistence as e:
            logging.warning(
                f"Could not write to file {self.__file_path}, reason: {str(e)}"
            )
            raise e
        logging.info(f"User with ID {uid} has been deleted.")

    def edit(self, user_id: str, username: str):
        current_users = self.get_all()
        for user in current_users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = username
        users_info = [(str(u.id), u.username, u.stocks) for u in current_users]
        users_json = json.dumps(users_info)
        try:
            with open(self.__file_path, "w") as f:
                f.write(users_json)
        except OSError as e:
            logging.warning(
                f"Could not edit user with ID '{user_id}' in file '{self.__file_path}'. Reason: {str(e)}"
            )
            raise ErrorWhenWritingInPersistence(e)
