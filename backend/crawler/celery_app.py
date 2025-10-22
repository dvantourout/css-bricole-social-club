from celery import Celery
from celery.schedules import crontab
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    "crawler",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["crawler.tasks"],
)

celery_app.conf.update(
    task_routes={
        "crawler.tasks.refresh_*": {"queue": "refresh"},
    },
)

celery_app.conf.beat_schedule = {
    "refresh-trending-queries": {
        "task": "crawler.tasks.refresh_trending_queries",
        "schedule": crontab(minute="*/30"),
        "options": {"queue": "refresh"},
    }
}
