from typing import Optional

from pydantic import BaseModel


class AgentInstanceCreate(BaseModel):
    pass


class AgentInstanceUpdate(BaseModel):
    bi_report_count: Optional[int]
