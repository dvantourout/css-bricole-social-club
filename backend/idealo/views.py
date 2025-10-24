from database import SessionDep
from fastapi import APIRouter
from idealo.client import Client
from idealo.repository import TrendingQueryRepository

router = APIRouter()
client = Client()


@router.get("/trending-queries")
def get_trending_queries(db_session: SessionDep):
    repository = TrendingQueryRepository(db_session)

    return repository.list(order_by="updated_at", order_by_desc=True)


@router.get("/sync")
def sync(db_session: SessionDep):
    repository = TrendingQueryRepository(db_session)
    queries = client.get_trending_queries()

    return repository.upsert(queries.queries)
