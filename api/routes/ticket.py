from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, WebSocket, WebSocketDisconnect, status
from opentelemetry import trace
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from lib.broadcast.ticket import broadcast_ticket_list
from lib.connection import ConnectionManager
from lib.helpers import generate_ticket_number
from models.ticket import Ticket
from models.ticket import TicketStatus as TicketStatusModel
from schemas.ticketSchema import TicketCreate, TicketRead, TicketStatus

router = APIRouter()
manager = ConnectionManager()

tracer = trace.get_tracer(__name__)


@router.post("/", response_model=TicketRead)
async def create_ticket(payload: TicketCreate, response: Response, db: AsyncSession = Depends(get_db)) -> Ticket:

    with tracer.start_as_current_span("create_ticket") as span:
        span.set_attribute("queued.id", payload.queue_id)
        ticket = Ticket(
            queue_id=payload.queue_id,
            ticket_number="",
            status=TicketStatus.waiting,
        )

        db.add(ticket)

        await db.flush()

        ticket.ticket_number = generate_ticket_number(ticket.id)

        span.set_attribute("queued.ticket_number", ticket.ticket_number)
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)

        await broadcast_ticket_list(db)

        response.status_code = status.HTTP_201_CREATED
        return ticket


@router.get("/", response_model=List[TicketRead])
async def list_tickets(
    response: Response, db: AsyncSession = Depends(get_db), queue_id: int | None = None
) -> list[Ticket]:
    with tracer.start_as_current_span("list_tickets"):
        stmt = select(Ticket)
        if queue_id is not None:
            stmt = stmt.where(Ticket.queue_id == queue_id)

        result = await db.execute(stmt)
        tickets = result.scalars().all()

        response.status_code = status.HTTP_200_OK
        return list(tickets)


@router.websocket("/ws")
async def tickets_websocket(websocket: WebSocket) -> None:
    await manager.connect(websocket)

    with tracer.start_as_current_span("websocket_connection"):
        try:
            while True:
                message = await websocket.receive_text()

                with tracer.start_as_current_span("websocket_message") as span:
                    span.set_attribute("ws.message", message)

        except WebSocketDisconnect:
            manager.disconnect(websocket)


@router.patch("/{ticket_id}", response_model=TicketRead)
async def update_ticket_status(
    ticket_id: int, new_status: TicketStatus, response: Response, db: AsyncSession = Depends(get_db)
) -> Ticket:
    with tracer.start_as_current_span("update_ticket") as span:
        span.set_attribute("ticket.id", ticket_id)
        span.set_attribute("ticket.status", new_status.value)
        result = await db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ticket = result.scalar_one_or_none()

        if not ticket:
            raise HTTPException(status_code=404, detail="Ticket not found")

        ticket.status = TicketStatusModel(new_status.value)
        db.add(ticket)
        await db.commit()
        await db.refresh(ticket)
        await broadcast_ticket_list(db)

        response.status_code = status.HTTP_200_OK
        return ticket
