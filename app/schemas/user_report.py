from pydantic.main import BaseModel


class UserReportCreate(BaseModel):
    pass


class UserReportUpdate(BaseModel):
    status: int
