from typing import Optional
from pydantic.main import BaseModel


class SyncLogCreate(BaseModel):
    name: str
    type: int
    agent_instance_id: int
    user_id: int
    progress: int = 0
    start_time: Optional[int] = 0 
    end_time: Optional[int] = 0
    
class SyncLogUpdate(BaseModel):
    name: Optional[str]
    type: Optional[int]
    agent_instance_id: Optional[int]
    user_id: Optional[int]
    progress: Optional[int]
    start_time: Optional[int]
    end_time: Optional[int]
    
