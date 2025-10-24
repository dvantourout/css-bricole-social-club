from fastapi import APIRouter
from ikom.client import Client
from ikom.normalizer import IkomNormalizer

router = APIRouter()
client = Client()


@router.get("/")
def get_products(query: str):
    products = client.list_products(query=query)

    normalized_products = [IkomNormalizer.normalize(product) for product in products]

    return normalized_products
