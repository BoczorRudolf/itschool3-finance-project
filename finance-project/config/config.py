import json

from domain.exceptions import InvalidPersistenceType
from persistence.user_file import UserPersistenceFile
from persistence.user_sqlite import UserPersistenceSqlite


def persistence_type_by_choosing(file_path):
    with open(file_path, "r") as f:
        json_config_info = f.read()
        user_config_choice = json.loads(json_config_info)

        if user_config_choice.get("persistence") == "sqlite":
            return UserPersistenceSqlite()
        elif user_config_choice.get("persistence") == "file":
            return UserPersistenceFile("main_users.json")
        else:
            raise InvalidPersistenceType(
                "Unknown persistence type, choose between sqlite or file in config.json"
            )
