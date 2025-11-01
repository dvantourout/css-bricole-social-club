from integrations.idealo.models import TrendingQuery
from integrations.idealo.schemas import TrendingQuerySchema
from shared.repository import BaseRepository, OrderBy
from sqlalchemy import insert
from sqlalchemy.future import select


class TrendingQueryRepository(BaseRepository):
    def upsert(self, trending_queries: list[TrendingQuerySchema]) -> list[str]:
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

        return [q["query_text"] for q in queries_to_insert]

    def list(self, *, order_bys: list[OrderBy] = None) -> list[TrendingQuery]:
        stmt = select(TrendingQuery)
        stmt = self._order_by(stmt, order_bys)

        return self.db.scalars(stmt).all()
