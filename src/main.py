from fastapi import FastAPI

from routes import base
from helpers.config import get_settings
from routes import data
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()


settings = get_settings()
# protocall to connect to the database
postgres_connection = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRAS_PORT}/{settings.POSTGRES_DATABASE}"

app.database_engine = create_async_engine(postgres_connection)
app.database_clint = sessionmaker(app.database_engine, 
                                  expire_on_commit=False, 
                                  class_=AsyncSession)


app.include_router(base.base_router)
app.include_router(data.data_router)