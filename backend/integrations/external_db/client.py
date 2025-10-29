import logging
from typing import Generator

from config import EXTERNAL_SQLALCHEMY_URI
from integrations.external_db.models import Listing
from sqlalchemy import NullPool, create_engine, select
from sqlalchemy.orm import Session, joinedload

logger = logging.getLogger(__name__)


class ExternalDatabaseClient:
    def __init__(self):
        self.engine = create_engine(
            EXTERNAL_SQLALCHEMY_URI,
            echo=True,
            poolclass=NullPool,
            connect_args={
                "options": "-c default_transaction_read_only=on",
            },
        )

    def get_session(self) -> Session:
        session = Session(self.engine)

        return session

    def fetch_listing(
        self,
        batch_size: int = 1000,
        last_sync_id: int = 0,
    ) -> Generator[list[Listing]]:
        with self.get_session() as session:
            current_last_id = last_sync_id
            offset = 0

            while True:
                stmt = (
                    select(Listing)
                    .join(Listing.catalogue)
                    .options(joinedload(Listing.catalogue))
                    .where(Listing.id > current_last_id)
                    .order_by(Listing.id.asc())
                    .limit(batch_size)
                    .offset(offset)
                )

                listings = session.scalars(stmt).all()

                if not listings:
                    break

                if listings:
                    yield listings

                if len(listings) < batch_size:
                    break

                offset += len(listings)
