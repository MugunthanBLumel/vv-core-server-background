
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
    guid: str
    update_hash: str
    agent_instance_user_id: int



