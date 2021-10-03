from typing import Optional
from pydantic.main import BaseModel
from app.conf import codes
from app.conf.codes import ITEM_TYPE_MAP


class BIFolder(BaseModel):
    pass

class BIFolderCreate(BaseModel):
    name: str
    source_folder_id: Optional[int]
    path: str
    agent_instance_id: int
    depth: int 
    guid: int
    
class BIFolderUpdate(BaseModel):
    pass

class AgentFolders(BaseModel):
    idx: int
    guid: str 
    agent_instance_user_id: int
    bi_report_count: int