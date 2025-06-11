from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str
    APP_VERSION: str

    # File upload settings
    FILE_ALLOWED_TYPES: list
    FILE_MAX_ALLOWED_SIZE: int
    FILE_CHUNK_SIZE: int
    # DB Config
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD:str
    POSTGRAS_PORT:int
    POSTGRES_DATABASE:str
    POSTGRES_HOST:str

    GENERATION : str
    EMBEDDING :str

    # OpenAI Config
    OPENAI_API_KEY :str = None
    OPENAI_URL :str = None
    COHERE_API_KEY :str = None

    GENERATION_MODEL_ID :str= None
    EMBEDDING_MODEL_ID :str= None
    EMBEDDING_MODEL_SIZE :int= None

    INPUT_DEFUALT_MAX_CHARACTERS  :int= None
    GENERATION_DEFAULT_MAX_OUTPUT_TOKENS :int= None
    GENERATION_DEFAULT_TEMPERATURE :float= None
    
    # ------Vector DB ------
    VECTOR_DATABASE_BACKEND :str
    VECTOR_DESTANCE_METHOD :str = None
    VECTOR_DATABASE_INDEX_THRESHOLD: int = 1000
    
    #============ Templates ==========
    
    DEFAULT_LANG:str
    PRIMARY_LANG:str

    class Config:
        env_file = ".env"
        extra = "allow"




def get_settings():
    return Settings()