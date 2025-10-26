import logging

from core.repository import ProductRepository
from database import SessionDep
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
def get_products(db_session: SessionDep):
    return ProductRepository(db=db_session).list()
