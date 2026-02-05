from typing import Annotated

from pydantic import BaseModel, ConfigDict, constr


class QueueCreate(BaseModel):
    name: Annotated[str, constr(min_length=1, strip_whitespace=True)]

    model_config = ConfigDict(from_attributes=True)


class QueueRead(BaseModel):
    id: int
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
