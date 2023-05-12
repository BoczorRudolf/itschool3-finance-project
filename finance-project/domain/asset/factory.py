import yahooquery
from domain.asset.asset import Asset
from domain.exceptions import InvalidTicker


class AssetFactory:

    @staticmethod
    def make_new(ticker: str, quantity: int = 0) -> Asset:
        try:
            t = yahooquery.Ticker(ticker)
            profile = t.summary_profile[ticker]
            if type(profile) not in [dict]:
                raise InvalidTicker(f"Invalid ticker {ticker}")
            name = AssetFactory.__extract_name(profile)
            country = profile["country"]
            sector = profile["sector"]
            return Asset(
                ticker=ticker,
                nr=0,
                name=name,
                country=country,
                sector=sector,
            )
        except InvalidTicker as e:
            raise e
        except Exception as e:
            raise ValueError(f"Could not create asset with ticker {ticker}") from e

    @staticmethod
    def __extract_name(profile: dict) -> str:
        summary = profile["longBusinessSummary"]
        words = summary.split(" ")
        first_2_words = words[0:2]
        name = " ".join(first_2_words)
        return name

    @classmethod
    def make_from_persistence(cls, info: tuple) -> Asset:
        return Asset(
            ticker=info[0],
            nr=info[1],
            name=info[2],
            country=info[3],
            sector=info[4],
        )