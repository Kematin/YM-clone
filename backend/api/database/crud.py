from typing import Any, List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import Base
from database.uow import SqlAlchemyUoW


class Database:
    def __init__(self, model: Base, db: AsyncSession):
        self._model = model
        self._db = db
        self._uow = SqlAlchemyUoW(db)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Any]:
        items = await self._db.execute(select(self._model).offset(skip).limit(limit))
        return items.scalars().all()

    async def get(self, id: UUID4 | int) -> Any:
        item = await self._db.execute(
            select(self._model).filter(self._model.id == str(id))
        )
        if item:
            return item.scalars().first()
        else:
            return False

    async def create(self, data: dict) -> None:
        db_data = self._model(**data)
        self._db.add(db_data)
        await self._uow.refresh(db_data)

    async def delete(self, id: UUID4 | int) -> bool:
        item = await self.get(id)
        if not item:
            return False

        await self._uow.delete(item)
        return True

    async def delete_all(self) -> None:
        items = await self.get_all()
        for item in items:
            await self._uow.delete(item)

    async def update(self, id: UUID4 | int, data: dict) -> Any:
        db_item = await self.get(id)

        if not db_item:
            return False

        for key, value in data.items():
            setattr(db_item, key, value)

        self._db.add(db_item)
        await self._uow.refresh(db_item)

        return db_item
