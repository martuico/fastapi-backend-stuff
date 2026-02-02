from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from lib.helpers import generate_ticket_number
from models.ticket import Ticket
from models.ticket import TicketStatus as TicketStatusModel
from schemas.ticketSchema import TicketCreate, TicketRead, TicketStatus

router = APIRouter()


@router.post("/", response_model=TicketRead)
async def create_ticket(payload: TicketCreate, db: AsyncSession = Depends(get_db)) -> Ticket:
    ticket = Ticket(
        queue_id=payload.queue_id,
        ticket_number="",
        status=TicketStatus.waiting,
    )
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)

    ticket.ticket_number = generate_ticket_number(ticket.id)
    await db.commit()
    await db.refresh(ticket)

    return ticket


@router.get("/", response_model=List[TicketRead])
async def list_tickets(queue_id: int | None = None, db: AsyncSession = Depends(get_db)) -> list[Ticket]:
    stmt = select(Ticket)
    if queue_id is not None:
        stmt = stmt.where(Ticket.queue_id == queue_id)

    result = await db.execute(stmt)
    tickets = result.scalars().all()
    return list(tickets)


@router.patch("/{ticket_id}", response_model=TicketRead)
async def update_ticket_status(ticket_id: int, status: TicketStatus, db: AsyncSession = Depends(get_db)) -> Ticket:
    result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = TicketStatusModel(status.value)
    db.add(ticket)
    await db.commit()
    await db.refresh(ticket)
    return ticket
