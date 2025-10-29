import logging

from core.repository import ProductRepository
from database import SessionDep
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_products(
    db_session: SessionDep,
    query: str = None,
    limit: int = 100,
    offset: int = 0,
):
    products, count = ProductRepository(db=db_session).list_with_count(
        query=query, limit=limit, offset=offset
    )

    return {
        "products": products,
        "limit": limit,
        "offset": offset,
        "count": count,
    }
