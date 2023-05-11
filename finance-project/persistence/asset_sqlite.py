import sqlite3
from typing import List
from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.exceptions import NonExistentAsset
from domain.user.user import User


class AssetPersistenceSqlite(AssetPersistenceInterface):
    def __init__(self, db_file: str) -> None:
        self.db_file = db_file

    def add_to_user(self, user: User, asset: Asset) -> None:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"INSERT INTO '{table}' (ticker, name, country, units) "
                               f"VALUES (?, ?, ?, ?)", (asset.ticker, asset.name, asset.country, asset.units))
            except sqlite3.OperationalError:
                cursor.execute(f"CREATE TABLE '{table}' "
                               f"(ticker TEXT PRIMARY KEY, "
                               f"name TEXT, country TEXT, units REAL)")
                cursor.execute(f"INSERT INTO '{table}' (ticker, name, country, units) "
                               f"VALUES (?, ?, ?, ?)", (asset.ticker, asset.name, asset.country, asset.units))
            conn.commit()

    def get_for_user(self, user: User) -> List[Asset]:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM '{table}'")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
                else:
                    raise e
        assets_info = cursor.fetchall()
        assets = [Asset(
            ticker=x[0],
            nr=x[3],
            name=x[1],
            country=x[2],
            sector="sec"
        ) for x in assets_info]
        return assets

    def delete_for_user(self, user: User, asset: Asset) -> None:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM '{table}' WHERE ticker = ?", (asset.ticker,))
            if cursor.rowcount == 0:
                raise NonExistentAsset(f"Asset with ticker '{asset.ticker}' does not exist for user {user.username}")
            conn.commit()