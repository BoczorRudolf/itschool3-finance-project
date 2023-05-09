import json
import uuid
from singleton import singleton

from domain.asset.repo import AssetRepo
from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User

@singleton
class UserRepo:
    def __init__(self, persistence: UserPersistenceInterface):
        print("init user repo ")
        self.__persistence = persistence
        self.__users = None

    def add(self, new_user: User):
        if self.__users is None:
            self.__users = self.__persistence.get_all()
        self.__persistence.add(new_user)
        self.__users.append(new_user)



    def get_all(self) -> list[User]:
        if self.__users is None:
            self.__users = self.__persistence.get_all()
        return self.__users


    def get_by_id(self, uid: str) -> User:
        if self.__users is None:
            self.__users = self.__persistence.get_all()
        for u in self.__users:
            if u.id == uuid.UUID(hex=uid):
                assets = AssetRepo().get_for_user(u)
                return User(
                    uuid=u.id,
                    username=u.username,
                    stocks=assets
                )


