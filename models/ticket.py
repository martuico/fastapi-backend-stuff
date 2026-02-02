from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class TicketStatus(PyEnum):
    waiting = "waiting"
    called = "called"
    served = "served"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    queue_id: Mapped[int] = mapped_column(Integer, index=True)

    ticket_number: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        unique=True,
    )

    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, name="ticket_status"),
        default=TicketStatus.waiting,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
