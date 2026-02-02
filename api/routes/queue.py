from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from models.queue import Queue
from schemas.queueSchema import QueueCreate, QueueRead

router = APIRouter()


@router.post("/", response_model=QueueRead)
async def create_queue(
    payload: QueueCreate,
    db: AsyncSession = Depends(get_db),
) -> Queue:
    queue = Queue(name=payload.name)

    db.add(queue)
    await db.commit()
    await db.refresh(queue)

    return queue


@router.get("/", response_model=List[QueueRead])
async def list_queues(
    db: AsyncSession = Depends(get_db),
) -> list[Queue]:
    result = await db.execute(select(Queue))
    return list(result.scalars())
