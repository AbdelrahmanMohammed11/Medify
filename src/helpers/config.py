from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    class Config:
        env_file = ".env"
        case_sensitive = True
        validate_assignment = True


def get_settings():
    return Settings()