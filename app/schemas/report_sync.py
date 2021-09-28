from pydantic import BaseModel
from typing import Optional
from app.schemas.bi_report import AgentReports
from app.schemas.bi_folder import BIFolderCreate

class IncomingReport(BaseModel):
    name: str
    description: str = ""
    report_id: str
    url: str = ""
    url_t: str = ""
    path: str
    meta: str = "{}"
    sync_metadata: str = "{}"
    agent_instance_users: set[int]
    guid: str
    source_folder_guid: str 
    update_hash: str

class ExistingReport(BaseModel):
    idx: int
    guid: str
    path: str
    update_hash: str
    agent_instance_users: set[int]

class ExistingFolder(BaseModel):
    idx: int
    guid: str
    user_report_count_map: dict[int,int] = {}
    agent_instance_users: set[int]

class InsertFolders(BaseModel):
    idx: int
    source_folder_guid: Optional[str]


class IncomingFolder(BaseModel):
    name: str
    path: str
    agent_instance_id: int
    depth: int 
    guid: str
    user_report_count_map: dict[int,int] = {}
    agent_instance_users: set[int]
    source_folder_guid: str
