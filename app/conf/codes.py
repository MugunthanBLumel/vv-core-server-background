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

path_delimiter: str = "//"

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

FOLDER_ROOT_LEVEL_DEPTH: int = 1
DEFAULT_WORKER_COUNT: int = 5
DEAD_LOCK_RETRY_LIMIT: int = 3

SYNC_STATUS: dict[str,int] = {
    "started": 102,
    "success": 10,
    "partially_completed": 104,
    "failed": 103,
    "in_queue": 101
}

SYNC_TYPE: dict[str,int] = {
    "admin_report_sync": 1,
    "user_report_sync": 2
}

REPORT_SYNC_STATUS: dict[str,int] = {
    "added": 50,
    "updated": 150,
    "granted": 200,
    "revoked": 250    
}
