import yfinance


class Asset:
    def __init__(self, ticker: str, nr: float, name: str, country: str, sector: str):
        self.ticker = ticker
        self.units = nr
        self.name = name
        self.country = country
        self.sector = sector
        self.info = yfinance.Ticker(ticker).fast_info

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.ticker!r})"

    @property
    def current_price(self) -> float:
        return round(self.info["lastPrice"], 2)

    @property
    def currency(self) -> str:
        return self.info["currency"]

    @property
    def today_low_price(self) -> float:
        return self.info["dayLow"]

    @property
    def today_high_price(self) -> float:
        return self.info["dayHigh"]

    @property
    def open_price(self) -> float:
        return self.info["open"]

    @property
    def closed_price(self) -> float:
        return self.info["previousClose"]

    @property
    def fifty_day_price(self) -> float:
        return self.info["fiftyDayAverage"]

    @property
    def percentage_difference_between_closed_and_current_price(self) -> str:
        difference = self.closed_price - self.current_price
        percentage_difference = (difference / self.closed_price) * 100
        if difference > 0:
            return f"The closed price {self.closed_price} is {percentage_difference:.2f}% higher than the current price {self.current_price}"
        elif difference < 0:
            return f"The closed {self.closed_price} is {abs(percentage_difference):.2f}% lower than current {self.current_price}"
        return "The values are the same"

    @property
    def avg_today_price(self) -> float:
        return (self.today_high_price + self.today_low_price) / 2