from datetime import timedelta

from crawler.models import TrendingQueryCssSync
from integrations.idealo.models import TrendingQuery
from shared.models import utc_now
from shared.repository import BaseRepository
from sqlalchemy import insert, or_, select


class CssSyncRepository(BaseRepository):
    def get_active_css_sources(self) -> list[str]:
        # TODO: config in db
        return ["adstrong", "ikom"]

    def initialize_css_sync_for_queries(self, query_texts: list[str]):
        active_sources = self.get_active_css_sources()

        sync_records = []
        for query_text in query_texts:
            for css_source in active_sources:
                sync_records.append(
                    {
                        "query_text": query_text,
                        "css_source": css_source,
                    }
                )

        if sync_records:
            self.db.execute(insert(TrendingQueryCssSync), sync_records)
            self.db.commit()

    def get_random_query_for_css(self, css_source: str) -> TrendingQuery | None:
        now = utc_now()
        one_day_ago = now - timedelta(days=1)

        stmt = (
            select(TrendingQuery)
            .join(TrendingQueryCssSync)
            .where(
                TrendingQueryCssSync.css_source == css_source,
                or_(
                    TrendingQueryCssSync.last_sync.is_(None),  # Never synced
                    TrendingQueryCssSync.last_sync
                    < one_day_ago,  # Synced more than a day ago
                ),
            )
            .order_by(TrendingQuery.popularity.desc())
            .limit(1)
        )

        return self.db.scalars(stmt).first()

    def mark_css_sync(self, query_text: str, css_source: str):
        stmt = select(TrendingQueryCssSync).where(
            TrendingQueryCssSync.query_text == query_text,
            TrendingQueryCssSync.css_source == css_source,
        )

        sync_record = self.db.scalar(stmt)

        if not sync_record:
            sync_record = TrendingQueryCssSync(
                query_text=query_text,
                css_source=css_source,
            )
            self.db.add(sync_record)

        now = utc_now()
        sync_record.last_sync = now

        self.db.commit()
