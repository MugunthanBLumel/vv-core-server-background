from typing import Type, Union
from urllib.parse import quote_plus

from sqlalchemy import String, Text
from sqlalchemy.dialects.mysql import MEDIUMTEXT as MY_SQL_MEDIUMTEXT
from sqlalchemy.dialects.oracle import CLOB as ORACLE_CLOB

from app.schemas.config import DatabaseConnection


class DatabaseDetails:
    """Details of the Database to construct the connection uri"""

    def __init__(self, details: DatabaseConnection) -> None:
        """Initialize the database detail attributes

        Parameters
        ----------
        details   : DBConnectionsParams
            Database connection configuration such as host, port, password, etc
        """
        self._username = details.username
        self._password = details.password
        self._host = details.host
        self._port = details.port
        self._name = details.name
        self._encoding = details.encoding
        self._type = details.database_type
        self._extra = details.extra


class MySql(DatabaseDetails):
    """Mysql database connection uri by extending to DatabaseDetails class"""

    def get_connection_url(self) -> str:
        """Return the Mysql database connection string

        Returns
        -------
        url    : str
            URL with dialect to establish the database connection
        """
        url: str = "mysql+mysqldb://%s:%s@%s:%d/%s?charset=%s" % (
            self._username,
            quote_plus(self._password),
            self._host,
            self._port,
            self._name,
            self._encoding,
        )
        if self._extra:
            url += "&" + self._extra
        return url


class PostgreSQL(DatabaseDetails):
    """Postgresql database connection uri by extending to DatabaseDetails class"""

    def get_connection_url(self) -> str:
        """Return the Postgresql database connection string

        Returns
        -------
        url    : str
            URL with dialect to establish the database connection
        """
        url: str = "postgresql+psycopg2://%s:%s@%s:%d/%s" % (
            self._username,
            quote_plus(self._password),
            self._host,
            self._port,
            self._name,
        )
        if self._extra:
            url += "&" + self._extra
        return url


class Oracle(DatabaseDetails):
    """Oracle database connection uri by extending to DatabaseDetails class"""

    def get_connection_url(self) -> str:
        """Return the Oracle database connection uri

        Returns
        -------
        url    : str
            URL with dialect to establish the database connection
        """
        url: str = "oracle+cx_oracle://%s:%s@%s:%s/%s" % (
            self._username,
            quote_plus(self._password),
            self._host,
            self._port,
            "orcl",
        )
        if self._extra:
            url += "&" + self._extra
        return url


class DatabaseHelper:
    """A class to define helper methods which responsible to set the values
    on column type"""

    @classmethod
    def get_char_seq_type(cls) -> Union[Type[Text], String]:
        """Returns the character sequence type based on the database

        Returns
        -------
        ColumnType
            Type of the column which used to store the character sequences
        """
        from app.conf.config import settings  # To avoid circular import error

        return Text if settings.DATABASE_TYPE.lower() != "oracle" else String(4000)

    @classmethod
    def get_long_char_seq_type(cls) -> Union[ORACLE_CLOB, MY_SQL_MEDIUMTEXT]:
        """Returns the long character sequence type based on the database

        Returns
        -------
        ColumnType
            Type of the column which used to store the long character sequences
        """
        from app.conf.config import settings  # To avoid circular import error

        db_name: str = settings.DATABASE_TYPE.lower()
        if db_name == "mysql":
            return MY_SQL_MEDIUMTEXT
        elif db_name == "oracle":
            return ORACLE_CLOB
        elif db_name == "postgresql":
            return Text
        elif db_name == "mssql":
            return Text
