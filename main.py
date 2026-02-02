from fastapi import FastAPI

from api.routes import queue, ticket

app = FastAPI(title="Queue Management System")

app.include_router(queue.router, prefix="/queues", tags=["Queues"])
app.include_router(ticket.router, prefix="/tickets", tags=["Tickets"])
