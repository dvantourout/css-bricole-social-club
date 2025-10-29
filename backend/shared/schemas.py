from pydantic import BaseModel


class NormalizedPrice(BaseModel):
    value: float
    currency: str


class NormalizedProduct(BaseModel):
    external_id: str

    # required field
    title: str
    image_link: str | None = None
    link: str
    cleaned_link: str | None = None
    price: float
    currency: str
    merchant_name: str
    brand: str

    # useful for displaying sales
    sale_price: float | None = None

    # required for comparison
    gtin: str | None = None
    mpn: str | None = None
