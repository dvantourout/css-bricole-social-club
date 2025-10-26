import logging

from database import SessionDep
from fastapi import APIRouter
from integrations.adstrong.client import Client
from integrations.adstrong.normalizer import AdstrongNormalizer
from pydantic import ValidationError
from shared.schemas import NormalizedProduct

router = APIRouter()
client = Client()

logger = logging.getLogger(__name__)


@router.get("/")
def get_products(db_session: SessionDep, query: str) -> list[NormalizedProduct]:
    response = client.list_products(query=query)

    normalized_products = []

    for product in response.products:
        try:
            normalized_products.append(
                AdstrongNormalizer.normalize(product),
            )
        except ValidationError as e:
            logger.error(e.errors())

    return normalized_products
