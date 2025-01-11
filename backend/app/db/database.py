from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from backend.app.db.db_config import db_settings


DATABASE_URL = db_settings.get_db_url()
SYNC_DATABASE_URL = db_settings.get_sync_db_url()

engine = create_async_engine(url=DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True 

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                await session.rollback() 
                raise e  
            finally:
                await session.close()
    return wrapper