from sqlalchemy import Select, asc, desc
from sqlalchemy.orm import Session


class OrderBy:
    def __init__(self, name: str, desc: bool = False):
        self.name = name
        self.desc = desc


class BaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def _order_by(self, stmt: Select, order_bys: list[OrderBy]) -> Select:
        if order_bys:
            for order_by in order_bys:
                order_by_direction = desc if order_by.desc else asc
                stmt = stmt.order_by(
                    order_by_direction(order_by.name),
                )

        return stmt
