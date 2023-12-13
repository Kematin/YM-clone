from typing import Annotated, Any, List

from fastapi import Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

from database.connection import Base, SessionLocal


# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


class Database:
    def __init__(self, model: Base, db: db_dependency):
        self.model = model
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def get(self, uuid: UUID4) -> Any:
        item = self.db.query(self.model).filter(self.model.id == str(uuid)).first()
        if item:
            return item
        else:
            return False

    def create(self, data: dict) -> None:
        db_data = self.model(**data)
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)
