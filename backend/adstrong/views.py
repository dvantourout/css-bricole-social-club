from adstrong.schemas import ProductsOutputs
from adstrong.service import list_products
from database import SessionDep
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_products(db_session: SessionDep) -> ProductsOutputs:
    return list_products(db_session=db_session, query="chaussures securite timberland")
