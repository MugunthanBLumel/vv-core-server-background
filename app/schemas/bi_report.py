from pydantic.main import BaseModel


class BIReportCreate(BaseModel):
    pass


class BIReportUpdate(BaseModel):
    pass


class BIReportDetails(BaseModel):
    idx: int
    path: str
    guid: str
    update_hash: str
    agent_instance_user_id: int
    user_bi_report_id: int
