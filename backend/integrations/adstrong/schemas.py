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
    # External id
    id: str

    title: str
    image: str
    url: str
    seller: str
    brand: str = None

    marketing_price: Optional[MarketingPriceSchema] = Field(
        alias="marketingPrice",
        default=None,
    )
    price: PriceSchema
    gtin: str = None
    mpn: str = None


class AdstrongProductsSchema(BaseModel):
    total: int
    total_sellers: int = Field(alias="totalSellers")
    products: list[ProductInputSchema]
