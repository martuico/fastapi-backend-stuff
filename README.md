# Queue Management System A REST API for managing queues, built with FastAPI, Pydantic, and SQLAlchemy. Supports database migrations with Alembic

## 🐍 Python Setup We recommend using pyenv to manage Python versions

This project requires Python 3.13.

```sh
# Install Python 3.13 using pyenv
pyenv install 3.13.0
pyenv local 3.13.0

# Create virtual environment
python3.13 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Update start.sh permission
chmod +x start.sh
```

## 📦 Install Dependencies

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Run the App

```sh
./start.sh
```

- The API will be available at: [Cotext: http://127.0.0.1:8000]
- Swagger docs: [Context: http://127.0.0.1:8000/docs]
- ReDoc: [Context: http://127.0.0.1:8000/redoc]

## 🗄 Database Migrations (Alembic) Create a

.env file in the project root:

```sh
DATABASE_URL=postgresql://mar-tuico:password@localhost:5432/queue_db
```

Make sure your alembic/env.py reads this environment variable. Create a migration

```sh
alembic revision -m "create tickets table"
```

Apply migrations

```sh
alembic upgrade head
```

Optional: Check current revision

```sh
alembic current
```

## ⚙️ Technologies Used

- Python 3.13
- FastAPI
– web framework for REST APIs
- Pydantic
– data validation and settings management
- SQLAlchemy
– ORM for database interactions
- Alembic
– database migrations
- PostgreSQL
– relational database

## 📝 Notes

- Use virtual environments to isolate project dependencies.
- Make sure the PostgreSQL database is running locally before applying migrations.
- Alembic is configured to read the database URL from .env.

### TODO

- [x] Add loggin and telemetry
- [x] Add JWT
- [x] Add Pub/Sub (No redis just memory)
- [ ] Add Dockerfile handles network, postgresql, fastapi and rabbitmq

## Per Requirement before project starts

Learning Plan & Next Steps

Timeline: 1–2 Weeks Focus: Backend proficiency with Python 3.13 & FastAPI

### Phase 1: Core Fundamentals (The "Stack")

- Language: Get comfortable with Python 3.13, focusing on modern typing
and async features.
- Framework: Go through FastAPI, specifically understanding the Pydantic model
system for data validation and schema definition.
- Database: Implement SQLAlchemy (ORM) and PostgreSQL.
- Migrations: Use Alembic for database migrations and schema management.

### Phase 2: Infrastructure & DevOps

- Containerization: Set up Docker Compose to orchestrate the application
and database containers.
- Security: Learn secret management using GCP (Google Cloud Platform) to
handle credentials securely.
- Observability: Implement basic Logging and Telemetry to understand
application health.

### Phase 3: The Practical Deliverable

Build a simple but complete CRUD application that demonstrates
understanding of the full lifecycle:

- HTTP Verbs: Implement all four standard methods: GET, POST, PUT/PATCH, and DELETE.
- Routing: Demonstrate how the routing system works in FastAPI (e.g., APIRouter).
- Environments: Set up configuration management for different
environments (Dev vs. Prod).
- Migrations: Successfully migrate the database schema using Alembic.
