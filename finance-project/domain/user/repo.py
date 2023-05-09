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
        print("Initialize UserRepo")
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
        for user in self.__users:
            if user.id == uuid.UUID(hex=uid):
                assets = AssetRepo().get_for_user(user)
                return User(
                    uuid=user.id,
                    username=user.username,
                    stocks=assets
                )

    def delete(self, uid: str):
        self.__check_we_have_users()
        self.__persistence.delete(uid)
        for user in self.__users:
            if user.id == uuid.UUID(hex=uid):
                self.__users.remove(user)
                break

    def update(self, user_id: str, username: str):
        self.__check_we_have_users()
        self.__persistence.update(user_id, username)
        for user in self.__users:
            if user.id == uuid.UUID(hex=user_id):
                user.username = username

    def __check_we_have_users(self):
        if self.__users is None:
            self.__users = self.__persistence.get_all()