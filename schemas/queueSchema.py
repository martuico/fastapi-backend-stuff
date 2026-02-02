from pydantic import BaseModel, ConfigDict


class QueueCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class QueueRead(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
