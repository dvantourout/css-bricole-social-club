from pydantic import BaseModel


class NormalizedPrice(BaseModel):
    value: float
    currency: str


class NormalizedProduct(BaseModel):
    # required field
    title: str
    image_link: str
    link: str
    price: NormalizedPrice
    merchant_name: str

    # useful for displaying sales
    sale_price: NormalizedPrice | None = None

    # required for comparison
    gtin: str | None = None
    mpn: str | None = None
