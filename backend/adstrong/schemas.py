import logging
from typing import Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Price(BaseModel):
    value: float
    currency: str


class MarketingPrice(BaseModel):
    original_price: Price = Field(alias="originalPrice", default=None)
    discount_percentage: float = Field(alias="discountPercentage")


class ProductInput(BaseModel):
    title: str
    image: str
    url: str
    seller: str

    marketing_price: Optional[MarketingPrice] = Field(
        alias="marketingPrice",
        default=None,
    )
    price: Price
    mpn: str = None

    # id: str
    # marketplace: Optional[str]
    # mpn: str = None
    # seller_id: str = Field(alias="sellerId", default=None)
    # seller: str
    # seller_display: str = Field(alias="sellerDisplay")
    # brand: str = None
    # is_sale: bool = Field(alias="isSale")
    # is_prime: bool = Field(alias="isPrime")
    # free_shipping: bool = Field(alias="freeShipping")


class AdstrongProducts(BaseModel):
    total: int
    total_sellers: int = Field(alias="totalSellers")
    products: list[ProductInput]
