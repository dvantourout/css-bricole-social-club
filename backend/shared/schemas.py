from typing import Optional

from pydantic import BaseModel


class NormalizedProduct(BaseModel):
    title: str

    gtin: Optional[str] = None
    mpn: Optional[str] = None

    image_url: str
    product_url: str
