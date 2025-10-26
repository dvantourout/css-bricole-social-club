from uuid import uuid4

from shared.models import Product
from shared.schemas import NormalizedProduct
from sqlalchemy import Select, asc, desc, insert, select
from sqlalchemy.orm import Session


class OrderBy:
    def __init__(self, name: str, desc: bool = False):
        self.name = name
        self.desc = desc


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _order_by(self, stmt: Select, order_bys: list[OrderBy]) -> Select:
        if order_bys:
            for order_by in order_bys:
                order_by_direction = desc if order_by.desc else asc
                stmt = stmt.order_by(
                    order_by_direction(order_by.name),
                )

        return stmt


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
