from pydantic import BaseModel


class AgentUserCreate(BaseModel):
    pass


class AgentUserUpdate(BaseModel):
    pass


class AgentUserDetails(BaseModel):
    idx: int
