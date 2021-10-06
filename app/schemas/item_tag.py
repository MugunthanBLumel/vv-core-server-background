from pydantic.main import BaseModel


class ItemTagCreate(BaseModel):
    pass


class ItemTagUpdate(BaseModel):
    status: int
