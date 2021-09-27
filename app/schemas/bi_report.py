
from pydantic.main import BaseModel
from app.conf import codes
from app.conf.codes import ITEM_TYPE_MAP

class BIReportCreate(BaseModel):
    pass


class BIReportUpdate(BaseModel):
    pass

class AgentReports(BaseModel):
    idx: int
    path: str 
    reportid_agentid_path_hash: str
    update_hash: str
    agent_user_id: int



