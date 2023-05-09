import json
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class UserPersistenceFile(UserPersistenceInterface):

    def __init__(self, file_path: str):
        self.__file_path = file_path

    def get_all(self) -> list[User]:

        try:
            file = open(self.__file_path)
            contents = file.read()
            file.close()
            users_info = json.loads(contents)
            factory = UserFactory()
            return [factory.make_from_persistance(x) for x in users_info]
        except:
            return []

    def add(self, user: User):
        current_users = self.get_all()
        current_users.append(user)
        users_info = [(str(x.id), x.username, x.stocks) for x in current_users]
        users_json = json.dumps(users_info)
        file = open(self.__file_path, "w")
        file.write(users_json)
        file.close()