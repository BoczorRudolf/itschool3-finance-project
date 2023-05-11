import logging
import uuid

from domain.exceptions import InvalidPersistenceInfo
from domain.user.user import User

class InvalidUsername(Exception):
    pass



class UserFactory:
    def make_new(self, username: str) -> User:
        if len(username) > 20:
            raise InvalidUsername(
                "The username field should be limited to a maximum of 20 characters."
            )
        if len(username) < 6:
            raise InvalidUsername(
                "The username must be a minimum of 6 characters in length. "
            )
        for char in username:
            if not (char.isalnum() or char == "-"):
                raise InvalidUsername(
                    "The username must consist solely of alphanumeric characters or the hyphen (-) symbol."
                )
        user_uuid = uuid.uuid4()
        return User(user_uuid, username)


    def make_from_persistence(self, info: tuple) -> User:
        if len(info) != 2:
            error_msg = "Persistence info should be a tuple with 2 elements"
            logging.error(error_msg)
            raise InvalidPersistenceInfo(error_msg)

        uuid_str, username = info
        try:
            user_uuid = uuid.UUID(uuid_str)
        except ValueError:
            error_msg = f"Invalid UUID: {uuid_str}"
            logging.error(error_msg)
            raise InvalidPersistenceInfo(error_msg)

        return User(user_uuid, username)


