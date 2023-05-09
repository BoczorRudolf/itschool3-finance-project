import json
import uuid

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class NonExistentUserId(Exception):
    pass


class UserPersistenceFile(UserPersistenceInterface):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path) as file:
                contents = file.read()
                users_info = json.loads(contents)
                factory = UserFactory()
                return [factory.make_from_persistance(x) for x in users_info]
        except:
            return []

    def write_file(self, current_users):
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        with open(self.file_path, "w") as file:
            file.write(users_json)

    def get_all(self) -> list[User]:
        current_users = self.read_file()
        return current_users

    def add(self, user: User):
        current_users = self.read_file()
        current_users.append(user)
        self.write_file(current_users)

    def get_by_id(self, uid: str) -> User:
        current_users = self.read_file()
        correct_id = [u for u in current_users if str(u.id) == uid]
        if not correct_id:
            raise NonExistentUserId(f"No user found with ID '{uid}'")

        for u in current_users:
            if u.id == uuid.UUID(hex=uid):
                assets = AssetRepo().get_for_user(u)

                return User(uuid=u.id, username=u.username, stocks=assets)

    def delete(self, uid: str):
        current_users = self.read_file()
        try:
            updated_users_list = [
                u for u in current_users if u.id != uuid.UUID(hex=uid)
            ]
        except ValueError:
            raise NonExistentUserId(f"No user found with ID '{uid}'")
        self.write_file(updated_users_list)

