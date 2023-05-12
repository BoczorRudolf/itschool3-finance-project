import unittest
from unittest.mock import MagicMock

from domain.asset.factory import AssetFactory


class TestAssetFactory(unittest.TestCase):

    def setUp(self):
        self.factory = AssetFactory()

    def test_make_new(self):
        chosen_ticker = "TSLA"
        profile_for_chosen_ticker = {
            "longBusinessSummary": "Tesla, Inc. is an American electric vehicle and clean energy company."
                                   "The company designs, manufactures, and sells electric cars, solar energy "
                                   "products, and more.",
            "country": "United States",
            "sector": "Consumer Cyclical"
        }

        mock_yahoo_ticker_instance = MagicMock()
        mock_yahoo_ticker_instance.summary_profile = {chosen_ticker: profile_for_chosen_ticker}
        mock_yahoo_ticker = MagicMock(return_value=mock_yahoo_ticker_instance)

        with unittest.mock.patch("yahooquery.Ticker", mock_yahoo_ticker):
            asset = self.factory.make_new(chosen_ticker)

        self.assertEqual(asset.ticker, chosen_ticker)
        self.assertEqual(asset.units, 0)
        self.assertEqual(asset.name, "Tesla, Inc.")
        self.assertEqual(asset.country, profile_for_chosen_ticker["country"])
        self.assertEqual(asset.sector, profile_for_chosen_ticker["sector"])

    def test_make_from_persistence(self):
        info = ("TESLA", 0, "Tesla, Inc.", "United States", "Technology")
        asset = self.factory.make_from_persistence(info)

        self.assertEqual(asset.ticker, info[0])
        self.assertEqual(asset.units, info[1])
        self.assertEqual(asset.name, info[2])
        self.assertEqual(asset.country, info[3])
        self.assertEqual(asset.sector, info[4])


if __name__ == '__main__':
    unittest.main()
