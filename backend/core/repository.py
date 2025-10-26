from uuid import uuid4

from core.models import Product
from shared.repository import BaseRepository
from shared.schemas import NormalizedProduct
from sqlalchemy import insert, select


class ProductRepository(BaseRepository):
    def upsert(self, *, source: str, products: list[NormalizedProduct]):
        products_to_insert: list = []

        products_external_id = [product.external_id for product in products]

        stmt = select(Product.external_id).where(
            Product.source == source,
            Product.external_id.in_(
                products_external_id,
            ),
        )
        existing_producs_ids = self.db.scalars(stmt).all()

        for product in products:
            if product.external_id in existing_producs_ids:
                continue

            products_to_insert.append(
                {
                    "id": uuid4(),
                    "source": source,
                    "title": product.title,
                    "image_link": product.image_link,
                    "link": product.link,
                    "cleaned_link": product.cleaned_link,
                    "price": product.price.value,
                    "sale_price": product.sale_price.value
                    if product.sale_price
                    else None,
                    "currency": product.price.currency,
                    "merchant_name": product.merchant_name,
                    "brand": product.brand,
                    "gtin": product.gtin,
                    "mpn": product.mpn,
                    "external_id": product.external_id,
                }
            )

        if products_to_insert:
            self.db.execute(
                insert(Product),
                products_to_insert,
            )

    def list(self, *, filter_cleaned_link: bool = True):
        stmt = select(Product)

        if filter_cleaned_link:
            stmt = stmt.where(Product.cleaned_link.isnot(None))

        return self.db.scalars(stmt).all()
