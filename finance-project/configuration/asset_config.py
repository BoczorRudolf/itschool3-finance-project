import json

from configuration.config import InvalidPersistence
from persistence.asset_file import AssetPersistenceFile
from persistence.asset_sqlite import AssetPersistenceSqlite


def set_asset_persistence_type(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
    user_config_choice = json.loads(content)
    persistence_type = user_config_choice.get("persistence")

    if persistence_type == "sqlite":
        return AssetPersistenceSqlite()
    elif persistence_type == "file":
        return AssetPersistenceFile("main_assets.json")
    else:
        message = f"Unknown persistence type '{persistence_type}', choose between 'sqlite' or 'file' in config.json"
        raise InvalidPersistence(message)
