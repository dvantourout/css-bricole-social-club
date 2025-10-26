from uuid import UUID

from database import Base
from shared.models import TimestampMixin
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Product(TimestampMixin, Base):
    __tablename__ = "product"
    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
        ),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, index=True)

    title: Mapped[str]
    image_link: Mapped[str]
    link: Mapped[str]
    cleaned_link: Mapped[str | None]
    price: Mapped[float]
    sale_price: Mapped[float | None]
    currency: Mapped[str]
    merchant_name: Mapped[str]
    brand: Mapped[str]
    gtin: Mapped[str | None]
    mpn: Mapped[str | None]

    source: Mapped[str]
    external_id: Mapped[str]
