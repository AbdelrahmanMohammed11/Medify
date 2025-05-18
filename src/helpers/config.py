from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application settings
    APP_NAME: str
    APP_VERSION: str

    # File upload settings
    FILE_ALLOWED_TYPES: list
    FILE_MAX_ALLOWED_SIZE: int

    class Config:
        env_file = ".env"




def get_settings():
    return Settings()