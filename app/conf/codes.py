""" Constant Codes File """
from datetime import datetime, timezone
from typing import Dict


def DEFAULT_TIME() -> int:
    """Returns the current timestamp

    Returns
    -------
    int
        Value of the current timestamp
    """
    return int(datetime.now(tz=timezone.utc).timestamp())

ITEM_TYPE_MAP: Dict[str, int] = {
    "user_folder": 1,
    "user_custom_url": 2,
    "hub_folder": 3,
    "bi_folder": 4,
    "bi_report": 5,
    "admin_custom_url": 6,
}

ENABLED: int = 10
DISABLED: int = 20
DELETED: int = 500
path_delimiter = "//"
FOLDER_ROOT_LEVEL_DEPTH = 1
DEFAULT_WORKER_COUNT = 5