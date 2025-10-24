from pydantic import BaseModel, Field, RootModel


class Price(BaseModel):
    value: str
    currency: str


class ProductInput(BaseModel):
    # required field
    title: str
    image_link: str = Field(alias="imageLink")
    link: str
    price: Price
    merchant_name: str = Field(alias="merchantName")

    # display sales
    sale_price: Price | None = Field(alias="salePrice", default=None)

    # required for comparison
    gtin: str | None = None
    mpn: str | None = None
