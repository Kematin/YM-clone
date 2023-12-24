from typing import Any, List

from pydantic import UUID4
from sqlalchemy.orm import Session

from database.connection import Base

db_dependency = Session


def close_db(func):
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        finally:
            self.db.close()

    return wrapper


class Database:
    def __init__(self, model: Base, db: db_dependency):
        self.model = model
        self.db = db

    @close_db
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        items = self.db.query(self.model).offset(skip).limit(limit).all()
        return items

    @close_db
    def get(self, id: UUID4 | int) -> Any:
        item = self.db.query(self.model).filter(self.model.id == str(id)).first()
        if item:
            return item
        else:
            return False

    @close_db
    def create(self, data: dict) -> None:
        db_data = self.model(**data)
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)

    @close_db
    def delete(self, id: UUID4 | int) -> bool:
        item = self.get(id)
        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True

    @close_db
    def delete_all(self) -> None:
        items = self.get_all()
        for item in items:
            self.db.delete(item)
            self.db.commit()

    @close_db
    def update(self, id: UUID4 | int, data: dict) -> Any:
        db_item = self.get(id)

        if not db_item:
            return False

        for key, value in data.items():
            setattr(db_item, key, value)

        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)

        return db_item
