from idealo.models import TrendingQuery
from sqlalchemy.orm import Session


class TrendingQueryRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_or_create(self, query_text: str, source: str):
        query = self.db.query(TrendingQuery).get(
            {"query_text": query_text, "source": source}
        )

        if not query:
            query = TrendingQuery(query_text=query_text, source=source)

            self.db.add(query)
            self.db.commit()

        return query
