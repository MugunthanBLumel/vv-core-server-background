"""Logging configuration file """
import logging
import sys
from typing import Any

from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record: Any) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame: Any = logging.currentframe()
        depth = 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class HubLogger:
    @classmethod
    def customize_logging(cls) -> Any:
        """
        Logging customization
        """
        level = "info"
        format = (
            "<level>{level: <8}</level>"
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>:"
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan>:"
            "<level>{message}</level>"
        )
        logger.remove()
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=False,
            level="ERROR",
            format=format,
        )
        logger.add(
            'C:\\VisualBi\\Bihub_3.0\\report_sync\\log\\a.txt',
            enqueue=True,
            backtrace=False,
            level="DEBUG",
            format=format,
        )
        logging.basicConfig(handlers=[InterceptHandler()], level=0)
        logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
        for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)
