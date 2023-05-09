from pydantic import BaseModel, Field
from uuid import UUID


class UserAdd(BaseModel):
    username: str = Field(description="Alphanumeric username between 6 and 20 chars")




class AssetAdd(BaseModel):
    ticker: str

class AssetInfoBase(BaseModel):
    ticker: str
    name: str
    country: str

    class Config:
        orm_mode = True

class AssetInfoUser(AssetInfoBase):
    units: float

class AssetInfoPrice(AssetInfoBase):
    current_price: float
    currency: str
    #avg_today_price: float
    #open_price: float
    closed_price: float
    fifty_day_price: float

class UserInfo(BaseModel):
    id: UUID
    username: str
    stocks: list[AssetInfoBase]

    class Config:
        allow_population_by_field_name = True
        orm_mode = True