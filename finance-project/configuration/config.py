import json

from domain.exceptions import InvalidPersistence
from persistence.user_file import UserPersistenceFile
from persistence.user_sqlite import UserPersistenceSqlite





def set_persistence_type(file_path: str):
    with open(file_path, "r") as f:
        json_config_info = f.read()
    user_config_choice = json.loads(json_config_info)

    persistence_type = user_config_choice.get("persistence")
    if persistence_type == "sqlite":
        return UserPersistenceSqlite()
    elif persistence_type == "file":
        return UserPersistenceFile("main_users.json")
    else:
        raise InvalidPersistence(
            f"Unknown persistence type '{persistence_type}', choose between sqlite or file in config.json"
        )
