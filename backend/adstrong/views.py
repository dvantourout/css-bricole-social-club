from adstrong.client import Client
from adstrong.normalizer import AdstrongNormalizer
from fastapi import APIRouter
from shared.schemas import NormalizedProduct

router = APIRouter()
client = Client()


@router.get("/")
def get_products() -> list[NormalizedProduct]:
    response = client.list_products(query="chaussures securite timberland")

    normalized_products = [
        AdstrongNormalizer.normalize(product) for product in response.products
    ]

    return normalized_products
