import json

from domain.exceptions import InvalidPersistenceType
from persistence.asset_sqlite import AssetPersistenceSqlite


def check_asset_persistence_type(file_path: str):
    with open(file_path, "r") as f:
        content = f.read()
    asset_config = json.loads(content)
    if asset_config.get("persistence") == "sqlite":
        return AssetPersistenceSqlite()
    elif asset_config.get("persistence") == "file":
        return AssetPersistenceSqlite()

    else:
        raise InvalidPersistenceType(
            "Unknown persistence type, choose between sqlite or file in config.json"
        )