import logging
import sqlite3
from domain.asset.asset import Asset
from domain.asset.asset_persistence_interface import AssetPersistenceInterface
from domain.exceptions import DuplicateAsset
from domain.user.user import User


class AssetPersistenceSqlite(AssetPersistenceInterface):
    def add_to_user(self, user: User, asset: Asset):
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            logging.info(f"Executing add_to_user command for user {user.username}...")
            try:
                cursor.execute(
                    f"INSERT INTO '{table}' (ticker, name, country, units, sector)"
                    f"VALUES ('{asset.ticker}', '{asset.name}', "
                    f"'{asset.country}', {asset.units}, '{asset.sector}')"
                )
                logging.info(
                    f"Successfully added asset {asset.ticker} to user {user.username}"
                )
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    logging.warning(f"Asset <{asset.ticker}> already in database!")
                    raise DuplicateAsset(
                        f"Asset <{asset.ticker}> already in database! "
                    )
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    logging.warning(
                        f"Failed executing command add_to_user to add asset to user {user.username} list."
                        f"Reason: " + str(e)
                    )
                    logging.info("Creating table...")
                    cursor.execute(
                        f"CREATE TABLE '{table}'"
                        f" (ticker TEXT PRIMARY KEY,"
                        f" name TEXT,"
                        f" country TEXT,"
                        f" units REAL,"
                        f" sector TEXT)"
                    )
                    logging.info(f"Inserting into {table}")
                    cursor.execute(
                        f"INSERT INTO '{table}' (ticker, name, country, units, sector)"
                        f"VALUES ('{asset.ticker}', '{asset.name}', "
                        f"'{asset.country}', {asset.units}, '{asset.sector}')"
                    )
                conn.commit()

    def get_all(self, user: User) -> list[Asset]:
        table = f"{user.id}-assets".replace("-", "_")
        with sqlite3.connect(f"main_users.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(f"SELECT * FROM '{table}'")
            except sqlite3.OperationalError as e:
                if "no such table" in str(e):
                    return []
                else:
                    raise e
            assets_info = cursor.fetchall()
        assets = [
            Asset(ticker=x[0], nr=x[3], name=x[1], country=x[2], sector="sec")
            for x in assets_info
        ]
        return assets

    def delete_for_user(self, user_id, asset):
        pass

    def get_for_user(self, u):
        pass

    def append(self, asset):
        pass

    def add(self, user, units):
        pass
