""" Dependency Generator and Helper function file for API Endpoint Controller """
from typing import Any, Generator

from fastapi import Request
from fastapi.security import HTTPBearer

from app.db.session import SessionLocal


def get_db() -> Generator:
    """
    Returns the DB Session Generator

    Returns:
    --------
    Generator
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class CurrentUser(HTTPBearer):
    def __init__(self) -> None:
        super(CurrentUser, self).__init__(auto_error=False)

    # TODO: To remove Any Type
    async def __call__(self, request: Request) -> Any:
        """This method gets the current user details from the API request.

        Parameters
        ----------
        request : Request
            API request

        Returns
        -------
        Any
            Contains current user details.
        """
        return request.get("current_user")
