import sqlite3
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User
from domain.user.factory import UserFactory
from persistence.user_file import NonExistentUserId


class UserPersistenceSqlite(UserPersistenceInterface):
    def __init__(self):
        self.conn = sqlite3.connect("main_users.db")
        self.cursor = self.conn.cursor()
        self.factory = UserFactory()

    def get_all(self) -> list[User]:
        try:
            self.cursor.execute("SELECT * FROM users")
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                return []
            else:
                raise e
        users_info = self.cursor.fetchall()
        users = [self.factory.make_from_persistance(x) for x in users_info]
        return users

    def add(self, user: User):
        try:
            self.cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}','{user.username}')")
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                self.cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)")
            else:
                raise e
            self.cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}','{user.username}')")
        self.conn.commit()

    def get_by_id(self, uid: str) -> User:
        self.cursor.execute(f"SELECT * FROM users WHERE id='{uid}'")

        user_info = self.cursor.fetchone()
        if not user_info:
            raise NonExistentUserId(f"No user found with ID '{uid}'")

        user = self.factory.make_from_persistance(user_info)

        return user

    def delete(self, uid: str):
        self.cursor.execute(f"SELECT id FROM users WHERE id='{uid}'")
        result = self.cursor.fetchone()
        if result is None:
            raise NonExistentUserId(f"No user found with ID '{uid}'")
        self.cursor.execute(f"DELETE FROM users WHERE id = '{uid}'")
        self.conn.commit()

