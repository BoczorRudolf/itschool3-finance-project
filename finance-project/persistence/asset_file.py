import json
import logging
from typing import List

from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.asset.factory import AssetFactory
from domain.user.user import User


class AssetFilePersistence(AssetPersistenceInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_all(self, new_user: User) -> List[Asset]:
        try:
            with open(self.file_path, "r") as f:
                assets_info = json.load(f)
            factory = AssetFactory()
            return [factory.make_from_persistence(x) for x in assets_info]
        except Exception as e:
            logging.warning("We couldn't read the file, reason: " + str(e))
            return []

    def add(self, new_user: User, asset: Asset):
        current_assets = self.get_all(new_user)
        current_assets.append(asset)
        assets_info = [
            (
                x.ticker,
                x.units,
                x.name,
                x.country,
                x.current_price,
                x.currency,
                x.closed_price,
                x.fifty_day_price,
                x.today_low_price,
                x.today_high_price,
                x.open_price,
                x.percentage_diff,
            )
            for x in current_assets
        ]
        assets_json = json.dumps(assets_info)
        with open(self.file_path, "w") as f:
            f.write(assets_json)

    def get_for_user(self, u):
        pass

    def add_to_user(self, user, asset):
        pass
