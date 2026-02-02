from enum import Enum

from pydantic import BaseModel


class TicketStatus(str, Enum):
    waiting = "waiting"
    called = "called"
    served = "served"


class TicketCreate(BaseModel):
    queue_id: int


class TicketRead(BaseModel):
    id: int
    queue_id: int
    ticket_number: str
    status: TicketStatus
