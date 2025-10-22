from adstrong.client import Client
from adstrong.schemas import ProductsOutputs
from database import SessionDep
from fastapi import APIRouter

router = APIRouter()
client = Client()


@router.get("/")
def get_products(db_session: SessionDep) -> ProductsOutputs:
    return client.list_products(
        db_session=db_session, query="chaussures securite timberland"
    )
