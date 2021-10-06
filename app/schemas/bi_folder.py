from typing import Optional

from pydantic.main import BaseModel


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


class BIFolderDetails(BaseModel):
    idx: int
    guid: str
    agent_instance_user_id: int
    bi_report_count: int
    user_bi_folder_id: int
