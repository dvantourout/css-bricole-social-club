from celery import Celery
from celery.schedules import crontab
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "crawler",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "crawler.tasks",
        "integrations.external_db.tasks",
    ],
)

celery_app.conf.update(
    task_routes={
        "crawler.tasks.refresh_*": {"queue": "refresh"},
        "crawler.tasks.sync_*": {"queue": "sync"},
        "crawler.tasks.crawl_*": {"queue": "crawl"},
    },
)

celery_app.conf.beat_schedule = {
    "refresh-trending-queries": {
        "task": "crawler.tasks.refresh_trending_queries",
        "schedule": crontab(minute="*/30"),
        "options": {"queue": "refresh"},
    },
    "sync-trending-queries": {
        "task": "crawler.tasks.sync_adstrong_products",
        "schedule": crontab(minute="*"),  # Every minute
        "options": {"queue": "sync"},
    },
    "crawl-affiliate-links": {
        "task": "crawler.tasks.crawl_affiliate_links",
        "schedule": crontab(minute="*"),  # Every minute
        "options": {"queue": "crawl"},
    },
}
