from typing import Optional

from pydantic.main import BaseModel


class SyncLogCreate(BaseModel):
    name: str
    type: int
    sync_batch_id: Optional[int] = None
    meta: str = "{}"
    agent_instance_id: Optional[int] = None
    user_id: int
    progress: int = 0
    start_time: Optional[int] = None
    end_time: Optional[int] = None


class SyncLogUpdate(BaseModel):
    progress: Optional[int]
    start_time: Optional[int]
    end_time: Optional[int]
    status: int
