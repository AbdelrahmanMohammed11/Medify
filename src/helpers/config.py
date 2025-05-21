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

    class Config:
        env_file = ".env"
        extra = "allow"




def get_settings():
    return Settings()