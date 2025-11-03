import logging

from crawler.tasks import crawl_affiliate_links, sync_adstrong_products
from crawler.tasks import refresh_trending_queries as task_refresh_trending_queries
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/refresh-trending-queries")
def refresh_trending_queries():
    task_refresh_trending_queries.delay()


@router.get("/trigger-sync")
def trigger_sync():
    sync_adstrong_products.delay()


@router.get("/clean-uncleaned-links")
def clean_uncleaned_links():
    crawl_affiliate_links()
