import logging
import uuid

from domain.exceptions import InvalidPersistenceInfo, InvalidUsername
from domain.user.user import User







class UserFactory:
    def make_new(self, username: str) -> User:
        logging.info("UserFactory making new user with username: %s", username)
        if len(username) > 20:
            logging.error("InvalidUsername: The username field should be limited to a maximum of 20 characters.")
            raise InvalidUsername(
                "The username field should be limited to a maximum of 20 characters."
            )
        if len(username) < 6:
            logging.error("InvalidUsername: The username must be a minimum of 6 characters in length.")
            raise InvalidUsername(
                "The username must be a minimum of 6 characters in length. "
            )
        for char in username:
            if not (char.isalnum() or char == "-"):
                logging.error("InvalidUsername: The username must consist solely of alphanumeric characters or the hyphen (-) symbol.")
                raise InvalidUsername(
                    "The username must consist solely of alphanumeric characters or the hyphen (-) symbol."
                )
        user_uuid = uuid.uuid4()
        new_user = User(user_uuid, username)
        logging.info("UserFactory successfully created new user with id: %s", str(user_uuid))
        return new_user



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


