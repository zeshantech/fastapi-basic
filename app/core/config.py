from functools import lru_cache
from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "dev"
    database_url: PostgresDsn
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    refresh_token_expire_days: int = 30
    verification_token_expire_minutes: int = 10
    redis_uri: str = "redis://localhost:6379/0"
    openai_api_key: str 


    @field_validator("database_url", mode="before")
    def _fix_scheme(cls, v: str) -> str:
        return v.replace("postgresql://", "postgres://", 1)

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore