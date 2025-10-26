from datetime import datetime, timezone
from uuid import UUID

from database import Base
from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=utc_now(), onupdate=utc_now()
    )


class Product(Base):
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
