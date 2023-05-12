from pydantic import BaseModel, Field
from uuid import UUID


class OrmModel(BaseModel):
    class Config:
        orm_mode = True


class UserAdd(OrmModel):
    username: str = Field(
        description="Alphanumeric username between 6 and 20 chars"
    )


class AssetAdd(OrmModel):
    ticker: str = Field(
        description="Unique series of letters that represent a company's stock or security"
    )
class UnitsAdd(BaseModel):
    units: float = Field(description="Units to add for asset, default is 0")

class AssetInfoBase(OrmModel):
    ticker: str = Field(
        description="Unique series of letters that represent a company's stock or security"
    )
    name: str = Field(
        description="Name of a company based on the ticker given"
    )
    country: str = Field(
        description="Country where a company is located based on the ticker given"
    )


class AssetInfoUser(AssetInfoBase):
    units: float = Field(
        description="Number of stocks or security a user has"
    )


class AssetInfoPrice(AssetInfoBase):
    current_price: float = Field(
        description="Current price of a stock or security"
    )
    currency: str
    open_price: float = Field(
        description="Price at which a stock or security begins trading"
    )
    avg_today_price: float = Field(
        default=None, description="Average today price"
    )
    today_low_price: float = Field(
        description="This refers to the minimum value at which a specific stock or security has been sold or exchanged."
    )
    today_high_price: float = Field(
        description="This refers to the maximum price at which a stock or security was sold"
    )
    closed_price: float = Field(
        description="Yesterday's last recorded price of a stock or security"
    )
    fifty_day_price: float = Field(
        description="Average price for fifty days"
    )
    percentage_difference_between_closed_and_current_price: str = Field(
        description="Percentage difference between closed price and current price"
    )


class UserInfo(OrmModel):
    id: UUID = Field(description="ID to identify a user")
    username: str
    stocks: list[AssetInfoBase] = Field(
        description="List of stocks that represent ownership in a publicly-traded company"
    )