from fastapi import APIRouter
from integrations.external_db.client import ExternalDatabaseClient

router = APIRouter()
client = ExternalDatabaseClient()


@router.get("/")
def get_products():
    products = client.fetch_listing()

    return products
