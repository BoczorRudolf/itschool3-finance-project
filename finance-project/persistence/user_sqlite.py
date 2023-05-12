import logging
import sqlite3

from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User
from domain.user.factory import UserFactory


class UserPersistenceSqlite(UserPersistenceInterface):

    def get_all(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
                else:
                    raise e
            users_info = cursor.fetchall()
            factory = UserFactory()
            users = [factory.make_from_persistence(x) for x in users_info]

        return users

    def add(self, user: User):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)")
                else:
                    raise e
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}', '{user.username}')")
            conn.commit()


    def delete_by_id(self, uid: str):
        try:
            with sqlite3.connect("main_users.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM users WHERE id='{uid}'")
                conn.commit()
        except sqlite3.OperationalError as e:
            logging.error("Failed to delete user from database: %s", str(e))
            raise e

    def get_by_id(self, uid: str) -> User:
        pass
        # try:
        #     with sqlite3.connect("main_users.db") as conn:
        #         cursor = conn.cursor()
        #         cursor.execute(f"SELECT * FROM users WHERE id='{uid}'")
        #         user_info = cursor.fetchone()
        #         if user_info:
        #             factory = UserFactory()
        #             user = factory.make_from_persistence(user_info)
        #             return user
        #         else:
        #             logging.warning("User with id '%s' not found in database", uid)
        #             return None
        # except sqlite3.OperationalError as e:
        #     logging.error("Failed to retrieve user from database: %s", str(e))
        #     raise e

    def edit(self, user_id: str, new_username: str):
        try:
            with sqlite3.connect("main_users.db") as conn:
                cursor = conn.cursor()
                cursor.execute(f"UPDATE users SET username='{new_username}' WHERE id='{user_id}'")
                conn.commit()
        except sqlite3.OperationalError as e:
            logging.error("Failed to edit user in database: %s", str(e))
            raise e

    # def add_to_user(self, uid: str, ticker: str, units: int):
    #     with sqlite3.connect("main_users.db") as conn:
    #         cursor = conn.cursor()
    #         try:
    #             cursor.execute(f"UPDATE stocks SET units = units + {units} WHERE id='{ticker}'")
    #             if cursor.rowcount == 0:
    #                 cursor.execute(f"INSERT INTO stocks (id, units) VALUES ('{ticker}', {units})")
    #         except sqlite3.OperationalError as e:
    #             if "no such table" in str(e):
    #                 cursor.execute("CREATE TABLE stocks (id TEXT PRIMARY KEY, units INTEGER NOT NULL)")
    #                 cursor.execute(f"INSERT INTO stocks (id, units) VALUES ('{ticker}', {units})")
    #             else:
    #                 raise e
    #         conn.commit()