from datetime import datetime
from uuid import UUID

from database import Base
from integrations.external_db.database import ExternalBase
from shared.models import TimestampMixin
from sqlalchemy import DateTime, ForeignKey, Integer, PrimaryKeyConstraint, String, Uuid
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Catalogue(ExternalBase):
    __tablename__ = "catalogues"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    name: Mapped[str]


class Listing(ExternalBase):
    __tablename__ = "listings"
    __table_args__ = (PrimaryKeyConstraint("id", "catalogue_id"),)

    id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str]
    feed_img_links: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    link: Mapped[str]
    price: Mapped[float]
    sale_price: Mapped[float]
    currency: Mapped[str]
    brand: Mapped[str | None]
    gtin: Mapped[str | None]
    mpn: Mapped[str | None]

    catalogue_id: Mapped[int] = mapped_column(Integer, ForeignKey("catalogues.id"))
    catalogue: Mapped["Catalogue"] = relationship()


class ExternalDbSyncMetadata(Base, TimestampMixin):
    __tablename__ = "external_db_sync_metadata"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_synced_listing_id: Mapped[int]
    last_sync_timestamp: Mapped[datetime] = mapped_column(DateTime)
    total_synced: Mapped[int]
    last_error: Mapped[str | None] = mapped_column(nullable=True)
