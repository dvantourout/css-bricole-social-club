import logging

from core.repository import ProductRepository
from crawler.celery_app import celery_app
from crawler.repository import CssSyncRepository
from database import get_db
from integrations.adstrong.client import AdstrongClient
from integrations.adstrong.normalizer import AdstrongNormalizer
from integrations.idealo.client import Client as IdealoClient
from integrations.idealo.repository import TrendingQueryRepository
from pydantic import ValidationError
from shared.schemas import NormalizedProduct

logger = logging.getLogger(__name__)


@celery_app.task(name="crawler.tasks.refresh_trending_queries")
def refresh_trending_queries():
    logger.info("Starting trending queries refresh...")

    with get_db() as db:
        idealo_client = IdealoClient()
        css_sync_repository = CssSyncRepository(db)

        trending_queries = idealo_client.get_trending_queries()
        trending_repository = TrendingQueryRepository(db)

        new_query_texts = trending_repository.upsert(trending_queries.queries)

        if new_query_texts:
            css_sync_repository.initialize_css_sync_for_queries(new_query_texts)

    logger.info("Trending queries refreshed")


@celery_app.task(name="crawler.tasks.sync_adstrong_products")
def sync_adstrong_products():
    logger.info("Starting Adstrong product sync...")

    with get_db() as db:
        css_sync_repository = CssSyncRepository(db)
        product_repository = ProductRepository(db)

        trending_query = css_sync_repository.get_random_query_for_css("adstrong")

        if not trending_query:
            logger.info("No trending queries available for Adstrong sync")
            return {"status": "no_queries", "synced": 0}

        logger.info(
            f"Syncing Adstrong products for query: '{trending_query.query_text}'"
        )

        adstrong_client = AdstrongClient()
        adstrong_response = adstrong_client.list_products(
            query=trending_query.query_text
        )

        normalized_products: list[NormalizedProduct] = []

        for product in adstrong_response.products:
            try:
                normalized_products.append(AdstrongNormalizer.normalize(product))
            except ValidationError as e:
                logger.error(f"Error normalizing Adstrong product: {e.errors()}")

        if normalized_products:
            product_repository.upsert(
                source="adstrong",
                products=normalized_products,
            )

            css_sync_repository.mark_css_sync(
                trending_query.query_text,
                "adstrong",
            )

            return {
                "status": "success",
                "query": trending_query.query_text,
                "total_fetched": len(normalized_products),
                "total_available": adstrong_response.total,
            }
        else:
            logger.info("No valid products found from Adstrong")

            css_sync_repository.mark_css_sync(
                trending_query.query_text,
                "adstrong",
            )

            return {"status": "no_products", "query": trending_query.query_text}
