from fastapi import FastAPI
from typing_extensions import Dict

from api.routes import queue, ticket
from telemetry import instrument_fastapi, setup_tracing

app = FastAPI(title="Queue Management System")


@app.post("/publish")
async def publish(msg: str) -> Dict[str, str]:
    return {"message": msg}


app.include_router(queue.router, prefix="/queues", tags=["Queues"])
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])

# check telemetry
setup_tracing()
instrument_fastapi(app)
