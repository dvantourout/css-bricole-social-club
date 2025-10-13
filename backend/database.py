from typing import Annotated, Generator

from config import SQLALCHEMY_URI
from fastapi import Depends
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import DeclarativeBase, Session


class Base(DeclarativeBase):
    pass


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        try:
            yield session
            session.commit()

        except Exception as e:
            session.rollback()
            raise e  # TODO: better way of doing this


engine = create_engine(SQLALCHEMY_URI, echo=True)

SessionDep = Annotated[Session, Depends(get_session)]
