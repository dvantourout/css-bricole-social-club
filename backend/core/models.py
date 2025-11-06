from uuid import UUID

from database import Base
from shared.models import TimestampMixin
from sqlalchemy import Index, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column


class Product(TimestampMixin, Base):
    __tablename__ = "product"
    __table_args__ = (
        # GIN index for full-text search
        Index(
            "idx_product_search_vector",
            "search_vector",
            postgresql_using="gin",
        ),
        # B-tree indexes for exact matches
        Index("idx_product_gtin", "gtin"),
        Index("idx_product_mpn", "mpn"),
        # Functional indexes for case-insensitive prefix matching
        Index(
            "idx_product_brand_lower",
            func.lower("brand"),
            postgresql_ops={"lower": "text_pattern_ops"},
        ),
        Index(
            "idx_product_merchant_lower",
            func.lower("merchant_name"),
            postgresql_ops={"lower": "text_pattern_ops"},
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)

    title: Mapped[str]
    image_link: Mapped[str | None]
    link: Mapped[str]
    cleaned_link: Mapped[str | None]
    price: Mapped[float]
    sale_price: Mapped[float | None]
    currency: Mapped[str]
    merchant_name: Mapped[str]
    brand: Mapped[str | None]
    gtin: Mapped[str | None]
    mpn: Mapped[str | None]

    source: Mapped[str]
    external_id: Mapped[str]

    search_vector: Mapped[str | None] = mapped_column(TSVECTOR, nullable=True)
