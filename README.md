# Queue Management System A REST API for managing queues, built with FastAPI, Pydantic, and SQLAlchemy. Supports database migrations with Alembic

## 🐍 Python Setup We recommend using pyenv to manage Python versions.

This project requires Python 3.13.

```sh
# Install Python 3.13 using pyenv
pyenv install 3.13.0
pyenv local 3.13.0

# Create virtual environment
python3.13 -m venv .venv

# Activate virtual environment
source .venv/bin/activate
```

## 📦 Install Dependencies

```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 Run the App

```sh
uvicorn main:app --reload
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

- [] Add loggin and telemetry
- [] Add Dockerfile handles network, postgresql, fastapi and rabbitmq
