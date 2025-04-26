import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

load_dotenv('.env')


class Envs:
    DATABASE_URL = os.getenv('DATABASE_URL')


engine = create_async_engine(Envs.DATABASE_URL)

AsyncSessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def get_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
