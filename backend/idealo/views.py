from database import SessionDep
from fastapi import APIRouter
from idealo.client import Client
from idealo.repository import TrendingQueryRepository

router = APIRouter()
client = Client()


@router.get("/")
def get_trending_queries(db_session: SessionDep):
    repository = TrendingQueryRepository(db_session)

    return repository.list()
