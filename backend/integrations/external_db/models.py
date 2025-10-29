from uuid import UUID

from integrations.external_db.database import ExternalBase
from sqlalchemy import ForeignKey, Integer, PrimaryKeyConstraint, String, Uuid
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
