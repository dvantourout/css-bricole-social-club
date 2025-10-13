from database import SessionDep
from fastapi import APIRouter
from idealo.service import list_trending_queries

router = APIRouter()


@router.get("/")
def get_trending_queries(db_session: SessionDep):
    return list_trending_queries(db_session=db_session)
