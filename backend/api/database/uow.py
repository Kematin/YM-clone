from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


# TODO custom excpetions
class SqlAlchemyUoW:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def commit(self) -> None:
        try:
            await self._db.commit()
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err

    async def rollback(self) -> None:
        try:
            await self._db.rollback()
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err

    async def delete(self, instance) -> None:
        try:
            await self._db.delete(instance)
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err
        await self.commit()

    async def refresh(self, instance) -> None:
        await self.commit()
        try:
            await self._db.refresh(instance)
        except SQLAlchemyError as err:
            raise SQLAlchemyError from err
