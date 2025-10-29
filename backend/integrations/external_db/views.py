from fastapi import APIRouter
from integrations.external_db.client import ExternalDatabaseClient
from integrations.external_db.tasks import sync_external_database

router = APIRouter()
client = ExternalDatabaseClient()


@router.get("/sync")
def get_products():
    sync_external_database.delay()
