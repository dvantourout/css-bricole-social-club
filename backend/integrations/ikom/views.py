import logging

from fastapi import APIRouter
from integrations.ikom.client import Client
from integrations.ikom.normalizer import IkomNormalizer
from pydantic import ValidationError

router = APIRouter()
client = Client()

logger = logging.getLogger(__name__)


@router.get("/")
def get_products(query: str):
    response = client.list_products(query=query)

    normalized_products = []

    for product in response:
        try:
            normalized_products.append(
                IkomNormalizer.normalize(product),
            )
        except ValidationError as e:
            logger.error(e.errors())

    return normalized_products
