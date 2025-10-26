import logging

from adstrong.client import Client
from adstrong.normalizer import AdstrongNormalizer
from database import SessionDep
from fastapi import APIRouter
from pydantic import ValidationError
from shared.repository import ProductRepository
from shared.schemas import NormalizedProduct

router = APIRouter()
client = Client()

logger = logging.getLogger(__name__)


@router.get("/")
def get_products(db_session: SessionDep) -> list[NormalizedProduct]:
    response = client.list_products(query="sechoir linge chauffant")

    normalized_products = []

    for product in response.products:
        try:
            normalized_products.append(
                AdstrongNormalizer.normalize(product),
            )
        except ValidationError as e:
            logger.error(e.errors())

    ProductRepository(db=db_session).upsert(
        source="adstrong",
        products=normalized_products,
    )

    return normalized_products
