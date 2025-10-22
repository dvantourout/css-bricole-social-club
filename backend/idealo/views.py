from database import SessionDep
from fastapi import APIRouter
from idealo.client import Client

router = APIRouter()
client = Client()


@router.get("/")
def get_trending_queries(db_session: SessionDep):
    return client.list_trending_queries(db_session=db_session)
