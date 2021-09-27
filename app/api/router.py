""" Logging Each request entry and exit time """
import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from loguru import logger


class TimedRoute(APIRoute):
    """Logging each user request, request process duration and response

    Parameters
    ----------
    APIRoute : Request handler
        custom route function is added to fastapi APIRouter class for logging
        the user requests.
    """

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            logger.info(
                f"{request.scope.get('method', '')} "
                f"- {request.scope.get('path', '')} - {round(duration, 3)} sec"
            )
            return response

        return custom_route_handler
