import logging
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
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
from shared.utils import clean_link

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


@celery_app.task(name="crawler.tasks.crawl_affiliate_links")
def crawl_affiliate_links():
    with get_db() as db:
        products_repository = ProductRepository(db)
        products = products_repository.list(
            filter_without_cleaned_link=True,
            limit=10,
        )

        for product in products:
            logger.info(f"resolve affiliate link: {product.link}")

            parsed_url = urlparse(product.link)
            query_params = parse_qs(parsed_url.query)

            product_link = product.link

            if parsed_url.netloc in {"www.awin1.com"}:
                product_link = str(
                    urlunparse(
                        parsed_url._replace(
                            query=urlencode(
                                {"p": query_params.get("p")},
                                doseq=True,
                            )
                        )
                    )
                )
            elif parsed_url.netloc in {"bdt9.net"}:
                product_link = str(
                    urlunparse(
                        parsed_url._replace(
                            query=urlencode(
                                {
                                    "si": query_params.get("si"),
                                    "li": query_params.get("li"),
                                    "dl": query_params.get("dl"),
                                },
                                doseq=True,
                            )
                        )
                    )
                )
            response = requests.get(product_link, allow_redirects=True)
            cleaned_link = clean_link(response.url)

            product.cleaned_link = cleaned_link
            db.commit()

            logger.info(f"cleaned link: {cleaned_link}")
