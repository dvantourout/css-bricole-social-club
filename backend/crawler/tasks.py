import logging

from crawler.celery_app import celery_app
from database import get_db
from idealo.client import Client as IdealoClient
from idealo.repository import TrendingQueryRepository

logger = logging.getLogger(__name__)


@celery_app.task(name="crawler.tasks.refresh_trending_queries")
def refresh_trending_queries():
    logger.info("Starting trending queries refresh...")

    with get_db() as db:
        idealo_client = IdealoClient()
        trending_queries = idealo_client.get_trending_queries()

        trending_queries_repository = TrendingQueryRepository(db)

        for trending_query_data in trending_queries.queries:
            trending_query = trending_queries_repository.find_or_create(
                query_text=trending_query_data.query,
                source="idealo",
            )

    logger.info("Trending queries refreshed")
