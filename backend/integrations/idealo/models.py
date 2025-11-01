from database import Base
from shared.models import TimestampMixin
from sqlalchemy.orm import Mapped, mapped_column


class TrendingQuery(Base, TimestampMixin):
    __tablename__ = "trending_queries"

    query_text: Mapped[str] = mapped_column(primary_key=True, unique=True)
    popularity: Mapped[int]
    locale: Mapped[str]
