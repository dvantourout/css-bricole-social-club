from datetime import datetime

from database import Base
from shared.models import TimestampMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class TrendingQueryCssSync(Base, TimestampMixin):
    __tablename__ = "trending_query_css_sync"
    __table_args__ = (
        UniqueConstraint("query_text", "css_source", name="uq_query_css"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    query_text: Mapped[str] = mapped_column(
        ForeignKey("trending_queries.query_text", ondelete="CASCADE"), nullable=False
    )
    css_source: Mapped[str]
    last_sync: Mapped[datetime] = mapped_column(nullable=True)
