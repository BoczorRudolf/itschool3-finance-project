import yahooquery
from domain.asset.asset import Asset


class AssetFactory:
    def make_new(self, ticker: str) -> Asset:
        t = yahooquery.Ticker(ticker)
        profile = t.summary_profile[ticker]
        name = self.__extract_name(profile)
        country = profile["country"]
        sector = profile["sector"]
        return Asset(
            ticker=ticker,
            nr=0,
            name=name,
            country=country,
            sector=sector,
        )

    def __extract_name(self, profile: dict) -> str:
        summary = profile["longBusinessSummary"]
        words = summary.split(" ")
        first_2_words = words[0:2]
        name = " ".join(first_2_words)
        return name

