""" Custom Exceptions """
from typing import Any, Dict, Optional

from fastapi import HTTPException
from starlette.responses import JSONResponse


class HTTP500Exception(HTTPException):
    """
    Exception to throw HTTP 500 Status

    Extends:
    -------
    HTTPException

    Arguments:
    ----------
        detail: Error message or dict
        headers: Optional additional Header
    """

    def __init__(
        self, description: str = "", headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.details = {
            "message": "Internal error",
            "error_description": description,
        }
        super().__init__(
            status_code=500,
            detail=self.details,
            headers=headers,
        )

    def __str__(self) -> str:
        return str(self.details)


class HTTP404Exception(HTTPException):
    """
    Exception to throw HTTP 404 Status

    Extends:
    -------
    HTTPException

    Arguments:
    ----------
        headers: Optional additional Header
    """

    def __init__(
        self, description: str = "", headers: Optional[Dict[str, Any]] = None
    ) -> None:
        self.details = {
            "message": "Requested resource/method not found",
            "error_description": description,
        }
        super().__init__(
            status_code=404,
            detail=self.details,
            headers=headers,
        )

    def __str__(self) -> str:
        return str(self.details)


class HTTP400Exception(HTTPException):
    """
    Exception to throw HTTP 400 Status

    Extends:
    -------
    HTTPException

    Arguments:
    ----------
        headers: Optional additional Header
    """

    def __init__(
        self,
        description: str = "",
        headers: Optional[Dict[str, Any]] = None,
        message: str = "",
    ) -> None:
        self.message = "Invalid request sent"
        self.details = {
            "message": message or self.message,
            "error_description": description,
        }
        super().__init__(
            status_code=400,
            detail=self.details,
            headers=headers,
        )

    def __str__(self) -> str:
        return str(self.details)


class DbException(Exception):
    """
    Exception to throw database errors

    Extends:
    -------
    Exception
    """

    def __init__(
        self,
        message: str = "",
    ) -> None:
        self.message = message
        super().__init__(
            self.message,
        )

    def __str__(self) -> str:
        return str(self.message)


class StopSyncException(Exception):
    """
    Exception to interupt sync execution

    Extends:
    -------
    Exception
    """

    def __init__(
        self,
        message: str = "",
    ) -> None:
        self.message = message
        super().__init__(
            self.message,
        )

    def __str__(self) -> str:
        return str(self.message)


class AuthenticationException(JSONResponse):
    """
    Exception to throw HTTP 401 Status

    Extend
    ----------
    JSONResponse
    """

    def __init__(self, description: str = "") -> None:
        super().__init__(
            content={
                "details": {
                    "message": "Authentication Error",
                    "error_description": description,
                }
            },
            status_code=401,
        )
