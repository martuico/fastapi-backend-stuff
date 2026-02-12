from typing import List

from fastapi import APIRouter, Depends, Response, status
from opentelemetry import trace
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from models.queue import Queue
from schemas.queueSchema import QueueCreate, QueueRead

router = APIRouter()


tracer = trace.get_tracer(__name__)


@router.post("/", response_model=QueueRead)
async def create_queue(
    payload: QueueCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> Queue:

    with tracer.start_as_current_span("create_queue"):
        queue = Queue(name=payload.name)

        db.add(queue)
        await db.commit()
        await db.refresh(queue)
        response.status_code = status.HTTP_201_CREATED
        return queue


@router.get("/", response_model=List[QueueRead])
async def list_queues(
    response: Response,
    db: AsyncSession = Depends(get_db),
) -> list[Queue]:

    with tracer.start_as_current_span("list_queues"):
        result = await db.execute(select(Queue))
        response.status_code = status.HTTP_200_OK
        return list(result.scalars())


# Get all realtime tickets from queue
# Booth A1 -> ticket 123: served
