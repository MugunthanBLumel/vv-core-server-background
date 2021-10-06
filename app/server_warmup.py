import logging

from loguru import logger
from tenacity import (after_log, before_log, retry, stop_after_attempt,
                      wait_fixed)

from app.db.session import engine

MAX_RETRY = 3
WAIT_TIME = 5
DEFAULT_LOGGER = logging.getLogger(__name__)


@retry(
    stop=stop_after_attempt(MAX_RETRY),
    wait=wait_fixed(WAIT_TIME),
    before=before_log(DEFAULT_LOGGER, logging.INFO),
    after=after_log(DEFAULT_LOGGER, logging.WARNING),
)
def check_db() -> None:
    try:
        # Check Database Connectivity
        logger.info("Checking Database Connectivity...")
        engine.connect()
        logger.info("Database Connection Successfull")
    except Exception as e:
        logger.exception(e)
        raise e


def license_check() -> None:
    try:
        pass
    except Exception as e:
        logger.exception(e)
        raise e


def es_check() -> None:
    try:
        pass
    except Exception as e:
        logger.exception(e)
        raise e


def mq_check() -> None:
    try:
        pass
    except Exception as e:
        logger.exception(e)
        raise e


def warm_up() -> None:
    check_db()
    license_check()
    es_check()
    mq_check()


if __name__ == "__main__":
    warm_up()
