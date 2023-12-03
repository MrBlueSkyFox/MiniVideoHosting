from typing import Optional, Union

from pydantic import HttpUrl, PostgresDsn, ValidationInfo, TypeAdapter
from pydantic.functional_validators import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @field_validator("SENTRY_DSN")
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if v is None or len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Union[PostgresDsn, str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> PostgresDsn:

        if isinstance(v, str):
            return v
        return TypeAdapter(PostgresDsn).validate_python("postgresql+asyncpg://"
                                                        "{user}:{password}"
                                                        "@{host}:5432{dbname}".format(
            user=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            dbname=f"/{values.data.get('POSTGRES_DB') or ''}"
        ))

    SAVE_DIR: str = r"C:\Users\Tigran\PycharmProjects\MiniVideoHosting\data"


settings = Settings()
