import logging
import sqlite3

from domain.user.factory import UserFactory
from domain.user.persistance_interface import UserPersistenceInterface
from domain.user.user import User


class UserPersistenceSqlite(UserPersistenceInterface):
    def get_all(self) -> list[User]:
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM users")
            except sqlite3.OperationalError as e:
                if 'no such table' in str(e):
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
                cursor.execute(f"INSERT INTO users (id, username) VALUES ('{user.id}','{user.username}')")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(f"Table users does not exist in database. Creating it...")
                    cursor.execute("CREATE TABLE users (id TEXT PRIMARY KEY, username TEXT NOT NULL)")
                    logging.info("Table users created in database.")
                else:
                    logging.error(f"Error adding user with id {user.id}: {e}")
                    raise e
            else:
                logging.info(f"User with id {user.id} and username {user.username} added to database.")
                conn.commit()

    def update(self, user_id: User.id, username: str):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                logging.info(f"Updating user with id {user_id} with new username: {username}")
                cursor.execute(f"UPDATE users SET (username)='{username}' WHERE id='{user_id}'")
            except sqlite3.OperationalError as e:
                logging.error(f"Error updating user with id {user_id}: {e}")
                raise e
            else:
                conn.commit()
                logging.info(f"User with id {user_id} successfully updated with new username: {username}")

    def delete(self, user_id: User.id):
        with sqlite3.connect("main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM users WHERE id='{user_id}'")
                user_info = cursor.fetchone()
                if user_info is None:
                    logging.warning(f"User with id {user_id} not found in database")
                    return 404
                else:
                    cursor.execute(f"DELETE FROM users WHERE id='{user_id}'")
            except sqlite3.OperationalError as e:
                logging.error(f"Error deleting user with id {user_id}: {e}")
                raise e
            else:
                conn.commit()
                logging.info(f"User with id {user_id} successfully deleted from database")
