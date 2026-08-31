# API Key Manager

A backend API Key Management System built using FastAPI and PostgreSQL.

# Features

- User Signup and Login
- JWT Authentication
- API Key Generation
- API Key Hashing
- API Key Revocation
- API Key Deletion
- API Key Expiration
- Rate Limiting
- Usage Logging
- Protected API Endpoints
- Usage Analytics
- Database Migrations using Alembic

# Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- JWT
- Argon2

# Project Structure

```text
api_key_manager/
├── app/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── middleware/
│   ├── models/
│   ├── routers/
│   └── schemas/
├── alembic/
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md