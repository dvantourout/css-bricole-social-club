import logging

from core.repository import ProductRepository
from database import SessionDep
from fastapi import APIRouter
from shared.utils import clean_link

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
        query=query,
        limit=limit,
        offset=offset,
        filter_sources_in=["adstrong"],
        filter_cleaned_link=True,
    )

    return {
        "products": products,
        "limit": limit,
        "offset": offset,
        "count": count,
    }


@router.get("/clean-links")
def clean_links(db_session: SessionDep):
    offset = 0
    product_repository = ProductRepository(db=db_session)

    while True:
        products = product_repository.list(
            filter_cleaned_link=True,
            offset=offset,
            filter_sources_in=["adstrong"],
        )

        if not products:
            break

        for product in products:
            product.cleaned_link = clean_link(product.cleaned_link)

        db_session.commit()

        offset += len(products)
