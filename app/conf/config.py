""" Config File """
from secrets import token_urlsafe
from typing import Any, Dict, List, Optional

from pydantic import BaseSettings, validator

from app.helpers.db_helper import MySql, Oracle, PostgreSQL
from app.schemas.config import DatabaseConnection


class Settings(BaseSettings):
    """Settings which will help us to define and validate all the settings in app"""

    API_PREFIX: str = "/v2"
    PROJECT_NAME: str = "BI Hub"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Token Configuration
    SECRET_KEY: str = token_urlsafe(32)
    ACCESS_TOKEN_TIME: int = 5
    REFRESH_TOKEN_TIME: int
    ALGORITHM: str = "HS256"

    # Logger Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE_SIZE: int = 10 * 1024 * 1024
    LOG_FILE_COUNT: int = 5

    # Database Configuration
    DATABASE_TYPE: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_ENCODING: str
    DATABASE_EXTRA: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_URI: Optional[str]
    DATABASE_DRIVER: Optional[str]
    SQLALCHEMY_DATABASE_URI: Optional[str]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_database_connection(
        cls, v: Optional[str], values: Dict[str, Any]
    ) -> Any:
        """Returns the full Database DSN based on the other variables"""
        database_url: str
        db_type: str = values.get("DATABASE_TYPE", "").lower()
        db_connection_details: DatabaseConnection = DatabaseConnection(
            username=values["DATABASE_USER"],
            password=values["DATABASE_PASSWORD"],
            host=values["DATABASE_HOST"],
            port=values["DATABASE_PORT"],
            name=values["DATABASE_NAME"],
            encoding=values["DATABASE_ENCODING"],
            database_type=values["DATABASE_TYPE"],
            extra=values["DATABASE_EXTRA"],
        )

        if db_type == "mysql":
            database_url = MySql(db_connection_details).get_connection_url()
        elif db_type == "postgres":
            database_url = PostgreSQL(db_connection_details).get_connection_url()
        elif db_type == "oracle":
            database_url = Oracle(db_connection_details).get_connection_url()
        return database_url

    """Config class is used to get configuration from the .env file."""

    @validator("REFRESH_TOKEN_TIME", pre=True)
    def check_refresh_token_time(cls, v: int) -> int:
        """This method check the refresh token time from the env file.
        If time is less then 30 minutes it set a default time of
        30 minutes.

        Parameters
        ----------
        v : Optional[str]
            Refresh token time

        Returns
        -------
        int
            Refresh token time based on the condition
        """
        if int(v) < 30 or v is None:
            return 30
        return int(v)

    class Config:
        """Other Configuration Class for Settings class"""

        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton Settings variable
settings = Settings()
