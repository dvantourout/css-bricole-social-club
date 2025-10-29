import logging

from core.repository import ProductRepository
from crawler.celery_app import celery_app
from database import get_db
from integrations.external_db.client import ExternalDatabaseClient
from integrations.external_db.models import ExternalDbSyncMetadata
from integrations.external_db.normalizer import ExternalDbNormalizer
from pydantic import ValidationError
from shared.models import utc_now
from shared.schemas import NormalizedProduct

logger = logging.getLogger(__name__)


@celery_app.task(name="crawler.tasks.sync_external_database")
def sync_external_database():
    logger.info("Starting external database sync")

    with get_db() as db:
        try:
            # TODO: add error handling, resume at last failed ID
            last_sync_id = 0

            external_client = ExternalDatabaseClient()
            product_repository = ProductRepository(db)

            total_processed = 0

            new_sync_metadata = ExternalDbSyncMetadata(
                last_sync_timestamp=utc_now(),
            )

            for batch in external_client.fetch_listing(
                batch_size=1000,
                last_sync_id=last_sync_id,
            ):
                logger.info(f"Processing batch of {len(batch)} listings")

                normalized_products: list[NormalizedProduct] = []
                for listing in batch:
                    try:
                        normalized_products.append(
                            ExternalDbNormalizer.normalize(listing),
                        )

                        new_sync_metadata.last_synced_listing_id = listing.id
                    except ValidationError as e:
                        logger.error(f"Error normalizing listing: {e.errors()}")

                if normalized_products:
                    product_repository.upsert(
                        source="external_db",
                        products=normalized_products,
                    )
                    db.commit()

                    total_processed += len(normalized_products)
                    logger.info(f"Upserted {len(normalized_products)} products")
                    logger.info(f"Total processed: {total_processed}")

                new_sync_metadata.total_synced = total_processed
                db.add(new_sync_metadata)
                db.commit()
        except Exception as e:
            logger.error(f"Error during external database sync: {e}")
