from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select, delete as sqlalchemy_delete, update as sqlalchemy_update
from sqlalchemy import select

from aiocache import cached, Cache
from aiocache.serializers import JsonSerializer

from typing import Any

from database import async_session_maker


class BaseDAO:
    model = None
            
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance
    
    @classmethod
    @cached(ttl=120, cache=Cache.MEMORY, serializer=JsonSerializer())
    async def find_one_or_none(cls, **filter_by) -> Any:
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except SQLAlchemyError as e:
                raise e
    
    @classmethod
    async def delete(cls, delete_all: bool = False, **filter_by):
        if not delete_all and not filter_by:
            raise ValueError("You need to give almost one item for delete")

        async with async_session_maker() as session:
            async with session.begin():
                query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount
            
    @classmethod
    async def update(cls, filter_by, **values):
        async with async_session_maker() as session:
            async with session.begin():
                query = (
                    sqlalchemy_update(cls.model)
                    .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                    .values(**values)
                    .execution_options(synchronize_session="fetch")
                )
                result = await session.execute(query)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return result.rowcount