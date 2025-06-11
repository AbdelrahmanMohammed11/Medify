from fastapi import FastAPI
from routes import base, nlp
from helpers.config import get_settings
from routes import data
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from stores.LLM.LLMProviderFactory import LLMProviderFactory
from stores.VectorDataBase.VectorDataBaseFactory import VectorDataBaseFactory
from stores.LLM.template.template_parser import TemplateParser


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
    vectordb_provider_factory = VectorDataBaseFactory(config=settings, 
                                                      db_client=app.database_clint) 
    
    # Generation Client
    app.generation_client = llm_provider_factory.get_provider(
        provider =settings.GENERATION 
        )
    app.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)
    
    
    # Embedding Client
    app.embedding_client = llm_provider_factory.get_provider(
        provider =settings.EMBEDDING 
        )
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,
                                             embedding_size=settings.EMBEDDING_MODEL_SIZE)
    
    
    # Vector DataBase Client
    app.vectordb_client = vectordb_provider_factory.create(settings.VECTOR_DATABASE_BACKEND)
    await app.vectordb_client.connect()
    
    
    # template parser
    app.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG,
    )




async def shutdown():
    await app.database_engine.dispose()
    await app.vectordb_client.disconnect()
"""
app.router.lifespan.on_startup.append(startup)
app.router.lifespan.on_shutdown.append(shutdown)
"""
app.on_event("startup")(startup)
app.on_event("shutdown")(shutdown)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)