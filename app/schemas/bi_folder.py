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
    agent_id: int
    depth: int 
    agent_id_path_hash: int
    sync_id: int
    
class BIFolderUpdate(BaseModel):
    pass

class AgentFolders(BaseModel):
    idx: int
    agent_id_path_hash: str 
    agent_user_id: int
    report_count: int