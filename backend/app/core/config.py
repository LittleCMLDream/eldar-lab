from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    APP_NAME: str = "ELDAR API"
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/eldar"
    SECRET_KEY: str = "dev-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
settings = Settings()