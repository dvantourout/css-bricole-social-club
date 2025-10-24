import logging
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class PriceSchema(BaseModel):
    value: float
    currency: str


class MarketingPriceSchema(BaseModel):
    original_price: PriceSchema = Field(alias="originalPrice", default=None)
    discount_percentage: float = Field(alias="discountPercentage")


class ProductInputSchema(BaseModel):
    title: str
    image: str
    url: str
    seller: str

    marketing_price: Optional[MarketingPriceSchema] = Field(
        alias="marketingPrice",
        default=None,
    )
    price: PriceSchema
    mpn: str = None


class AdstrongProductsSchema(BaseModel):
    total: int
    total_sellers: int = Field(alias="totalSellers")
    products: list[ProductInputSchema]
