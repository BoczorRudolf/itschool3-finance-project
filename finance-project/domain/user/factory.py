
import uuid
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

    def make_from_persistance(self, info: tuple) -> User:
        return User(
            uuid=uuid.UUID(info[0]),
            username=info[1],
        )

