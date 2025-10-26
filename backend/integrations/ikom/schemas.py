from pydantic import BaseModel, Field


class PriceSchema(BaseModel):
    value: float
    currency: str


class ProductInputSchema(BaseModel):
    # required field
    title: str
    image_link: str = Field(alias="imageLink")
    link: str
    price: PriceSchema
    merchant_name: str = Field(alias="merchantName")
    brand: str

    # display sales
    sale_price: PriceSchema | None = Field(alias="salePrice", default=None)

    # required for comparison
    gtin: str | None = None
    mpn: str | None = None
