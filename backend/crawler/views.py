import logging

from crawler.tasks import refresh_trending_queries as task_refresh_trending_queries
from crawler.tasks import sync_adstrong_products
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/refresh-trending-queries")
def refresh_trending_queries():
    task_refresh_trending_queries.delay()


@router.get("/trigger-sync")
def trigger_sync():
    sync_adstrong_products.delay()
