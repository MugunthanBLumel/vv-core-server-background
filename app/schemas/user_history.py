from pydantic.main import BaseModel


class UserHistoryCreate(BaseModel):
    pass


class UserHistoryUpdate(BaseModel):
    status: int
