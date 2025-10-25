import logging

from adstrong.client import Client
from adstrong.normalizer import AdstrongNormalizer
from fastapi import APIRouter
from pydantic import ValidationError
from shared.schemas import NormalizedProduct

router = APIRouter()
client = Client()

logger = logging.getLogger(__name__)


@router.get("/")
def get_products() -> list[NormalizedProduct]:
    response = client.list_products(query="sechoir linge chauffant")

    normalized_products = []

    for product in response.products:
        try:
            normalized_products.append(
                AdstrongNormalizer.normalize(product),
            )
        except ValidationError as e:
            logger.error(e.errors())

    return normalized_products
