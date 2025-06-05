from fastapi import FastAPI
from routes import base
from helpers.config import get_settings
from routes import data
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from stores.LLM.LLMProviderFactory import LLMProviderFactory

app = FastAPI()
async def startup():
    settings = get_settings()


    # protocall to connect to the database
    postgres_connection = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRAS_PORT}/{settings.POSTGRES_DATABASE}"
    # make connection to the database
    app.database_engine = create_async_engine(postgres_connection)
    # create a session to the database
    app.database_clint = sessionmaker(app.database_engine, 
                                    expire_on_commit=False, 
                                    class_=AsyncSession)
    
    llm_provider_factory = LLMProviderFactory(settings)
    
    # Generation Client
    app.generation_client = llm_provider_factory.get_provider(
        provider =settings.GENERATION 
        )
    
    # Embedding Client
    app.embedding_client = llm_provider_factory.get_provider(
        provider =settings.EMBEDDING 
        )
    app.embedding_client.set_embedding_model(
        model_id= settings.EMBEDDING_MODEL_ID,
        embedding_size= settings.EMBEDDING_SIZE
        
    )





async def shutdown():
    app.database_engine.dispose()

app.on_event("startup")(startup)
app.on_event("shutdown")(shutdown)

app.include_router(base.base_router)
app.include_router(data.data_router)