from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.connection import ConnectionManager  # make sure manager is global
from models.ticket import Ticket

manager = ConnectionManager()


async def broadcast_ticket_list(db: AsyncSession) -> None:
    result = await db.execute(select(Ticket))
    tickets = result.scalars().all()

    data = [
        {
            "id": t.id,
            "queue_id": t.queue_id,
            "ticket_number": t.ticket_number,
            "status": t.status.value,
        }
        for t in tickets
    ]

    await manager.broadcast_json(data)
