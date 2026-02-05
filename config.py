from typing import Annotated

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):  # type: ignore[misc]
    ENV: Annotated[str, Field(default="dev")]
    DATABASE_URL: Annotated[str, Field()]
    OTEL_EXPORTER_URL: Annotated[AnyHttpUrl, Field(default="http://localhost:4318/v1/traces")]
    LOG_LEVEL: Annotated[str, Field(default="DEBUG")]
    DB_DEBUG: Annotated[bool, Field(default=False)]

    model_config = SettingsConfigDict(
        env_file=(".env"),
    )
