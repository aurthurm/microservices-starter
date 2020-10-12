import secrets
import os
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


def getenv_boolean(var_name, default_value=False):
    result = default_value
    env_value = os.getenv(var_name)
    if env_value is not None:
        result = env_value.upper() in ("TRUE", "1")
    return result

def getenv_value(value, default_value=None):    
    env_value = os.getenv(value)
    if env_value is None:
        env_value = default_value
    return env_value


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = getenv_value("SERVER_NAME", 'users')
    SERVER_HOST: AnyHttpUrl = getenv_value("SERVER_HOST", 'https://localhost')
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ['http://localhost:8000']

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = getenv_value("PROJECT_NAME", 'USERS PROJECT')
    SENTRY_DSN: Optional[HttpUrl] = getenv_value("SENTRY_DSN", "")

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str = getenv_value("POSTGRES_SERVER", 'users_db')
    POSTGRES_USER: str = getenv_value("POSTGRES_USER", 'users_admin')
    POSTGRES_PASSWORD: str = getenv_value("POSTGRES_PASSWORD", 'Access123')
    POSTGRES_DB: str = getenv_value("POSTGRES_DB", 'users_db')
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    
    EMAILS_ENABLED: bool = False
    
    FIRST_SUPERUSER_FIRSTNAME: str = getenv_value("FIRST_SUPERUSER_FIRSTNAME", 'System')
    FIRST_SUPERUSER_LASTNAME: str = getenv_value("FIRST_SUPERUSER_LASTNAME", 'Administrator')
    FIRST_SUPERUSER_EMAIL: EmailStr = getenv_value("FIRST_SUPERUSER_EMAIL", 'systemadmin@admin.com')
    FIRST_SEPERUSER_USERNAME: str = getenv_value("FIRST_SEPERUSER_USERNAME", 'systemadmin')
    FIRST_SUPERUSER_PASSWORD: str = getenv_value("FIRST_SUPERUSER_PASSWORD", 'SAccess123$')
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True

settings = Settings()