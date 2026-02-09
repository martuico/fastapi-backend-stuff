from typing import Annotated

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    ENV: Annotated[str, Field(default="dev")]
    DATABASE_URL: Annotated[str, Field()]
    DATABASE_URL_SYNC: Annotated[str, Field()]
    OTEL_EXPORTER_URL: Annotated[AnyHttpUrl, Field(default="http://localhost:4318/v1/traces")]
    LOG_LEVEL: Annotated[str, Field(default="DEBUG")]
    DB_DEBUG: Annotated[bool, Field(default=False)]
    SECRET_KEY: str
    ALGORITHM: Annotated[str, Field(default="HS256")]
    ACCESS_TOKEN_EXPIRE_MINUTES: Annotated[int, Field(default=30)]

    model_config = SettingsConfigDict(
        env_file=(".env"),
    )
