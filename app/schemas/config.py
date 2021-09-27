from typing import NamedTuple


class DatabaseConnection(NamedTuple):
    """A class to define the database connection configuration details"""

    username: str
    password: str
    host: str
    port: int
    name: str
    encoding: str
    database_type: str
    extra: str
