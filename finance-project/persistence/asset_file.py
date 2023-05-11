import json
import logging
from typing import List


from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset

from domain.user.user import User


logger = logging.getLogger(__name__)


class AssetPersistenceFile(AssetPersistenceInterface):
    def __init__(self, filename: str):
        self.__filename = filename

    def add_to_user(self, user: User, asset: Asset) -> None:
        data = self.__load_json()
        user_assets = data.get(str(user.id), [])
        for every_dict in user_assets:
            if every_dict["ticker"] == asset.ticker:
                raise DuplicateAsset(f"Asset {asset.ticker} already added")
        user_assets.append(
            {
                "ticker": asset.ticker,
                "name": asset.name,
                "country": asset.country,
                "nr": asset.units,
                "sector": asset.sector,
            }
        )
        data[str(user.id)] = user_assets
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Asset {asset.ticker} added to user {user.id}")

    def delete_for_user(self, user_id: str, asset_ticker: str) -> None:
        data = self.__load_json()
        if user_id in data:
            for d in data[user_id]:
                if d["ticker"] == asset_ticker:
                    data[user_id].remove(d)
                    break
        with open(self.__filename, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Asset {asset_ticker} deleted for user {user_id}")

    def get_for_user(self, user: User) -> List[Asset]:
        data = self.__load_json()
        user_assets = data.get(str(user.id), [])
        assets = []
        for asset_dict in user_assets:
            asset = Asset(
                ticker=asset_dict["ticker"],
                name=asset_dict["name"],
                country=asset_dict["country"],
                nr=asset_dict["nr"],
                sector=asset_dict["sector"],
            )
            assets.append(asset)
        logger.info(f"Assets retrieved for user {user.id}")
        return assets

    def __load_json(self) -> dict[str, list[dict[str, any]]]:
        try:
            with open(self.__filename) as f:
                return json.load(f)
        except FileNotFoundError as e:
            logging.warning(
                "Could not read file because it not exists, will return empty dict, reason: "
                + str(e)
            )
            return {}