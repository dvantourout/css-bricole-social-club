from idealo.models import TrendingQuery
from idealo.schemas import TrendingQuerySchema
from sqlalchemy import asc, desc, insert
from sqlalchemy.future import select
from sqlalchemy.orm import Session


class TrendingQueryRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_or_create(self, query_text: str, locale: str):
        query = self.db.query(TrendingQuery).get(
            {
                "query_text": query_text,
                "locale": locale,
            }
        )

        if not query:
            query = TrendingQuery(
                query_text=query_text,
                locale=locale,
            )

            self.db.add(query)
            self.db.commit()

        return query

    def upsert(self, trending_queries: list[TrendingQuerySchema]):
        queries = {query.query: query for query in trending_queries}

        stmt = select(TrendingQuery).where(
            TrendingQuery.query_text.in_(
                queries.keys(),
            ),
        )
        existing_queries = self.db.scalars(stmt).all()

        for existing_query in existing_queries:
            query = queries.pop(existing_query.query_text)

            existing_query.popularity = query.popularity

        queries_to_insert: list = []

        for _, query in queries.items():
            queries_to_insert.append(
                {
                    "query_text": query.query,
                    "popularity": query.popularity,
                    "locale": "fr_FR",
                }
            )

        self.db.execute(
            insert(TrendingQuery),
            queries_to_insert,
        )
        self.db.commit()

    def list(
        self, *, order_by: str = None, order_by_desc: bool = False
    ) -> list[TrendingQuery]:
        query = self.db.query(TrendingQuery)

        if order_by:
            order_by_direction = desc if order_by_desc else asc
            query = query.order_by(
                order_by_direction(order_by),
            )

        return query.all()
