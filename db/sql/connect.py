from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

URL = 'postgresql+asyncpg://postgres:boot@localhost:7432/qik_sql'
engine = create_async_engine(URL, echo=True)

AsyncSessionMaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
