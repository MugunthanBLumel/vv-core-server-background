from pydantic import BaseModel
from typing import NamedTuple, Optional,List,Tuple
from app.schemas.bi_report import AgentReports
from app.schemas.bi_folder import BIFolderCreate

class IncomingReport(NamedTuple):
    name: str
    description: str 
    report_id: str
    url: str 
    url_t: str 
    path: str
    meta: str 
    sync_metadata: str 
    agent_instance_users: List[int]
    guid: str
    update_hash: str

class InsertReport(NamedTuple):
    name: str
    description: str 
    report_id: str
    url: str 
    url_t: str 
    path: str
    meta: str 
    sync_metadata: str 
    guid: str
    update_hash: str
class UpdateReport(NamedTuple):
    name: str
    description: str 
    report_id: str
    url: str 
    url_t: str 
    path: str
    meta: str 
    sync_metadata: str 
    update_hash: str
    
    




class ExistingReport(BaseModel):
    idx: int
    guid: str
    path: str
    update_hash: str
    agent_instance_user_details: dict[int,int]

class FolderUserDetails(NamedTuple):
    user_bi_folder_id: int
    bi_report_count: int


class ExistingFolder(BaseModel):
    idx: int
    guid: str
    agent_instance_user_details: dict[int,FolderUserDetails]

class InsertFolders(BaseModel):
    idx: int
    source_folder_guid: Optional[str]


class IncomingFolder(BaseModel):
    name: str
    path: str
    agent_instance_id: int
    depth: int 
    guid: str
    user_report_count_map: dict[int,int] 
    agent_instance_users: List[int]
    

class FolderReportCountUpdate(NamedTuple):
    user_bi_folder_id: int
    bi_report_count: int