# FastAPI Patient Management System

A REST API built with FastAPI, SQLAlchemy, JWT Authentication, and SQLite for managing patient records.

## Features

- User Authentication
  - User Signup
  - User Login
  - JWT Token Authentication

- Patient Management
  - Create Patient
  - Get All Patients
  - Get Patient by ID
  - Update Patient
  - Delete Patient

- Database Integration
  - SQLAlchemy ORM
  - SQLite Database

- Interactive API Documentation
  - Swagger UI
  - ReDoc

---

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Passlib (Password Hashing)
- Pydantic

---

## Project Structure

```text
.
├── main.py
├── database.py
├── models.py
├── schemas.py
├── requirements.txt
├── patients.db
├── README.md
└── .gitignore
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/patient-management-api.git

cd patient-management-api
```

### Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Locally

```bash
uvicorn main:app --reload
```

Application:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

## Authentication Flow

### Register User

```http
POST /signup
```

Example:

```json
{
  "username": "admin",
  "password": "password123"
}
```

### Login

```http
POST /login
```

Example:

```json
{
  "username": "admin",
  "password": "password123"
}
```

Response:

```json
{
  "access_token": "JWT_TOKEN",
  "token_type": "bearer"
}
```

---

## Patient Endpoints

### Create Patient

```http
POST /patients
```

### Get All Patients

```http
GET /patients
```

### Get Patient

```http
GET /patients/{id}
```

### Update Patient

```http
PATCH /patients/{id}
```

### Delete Patient

```http
DELETE /patients/{id}
```

---

## Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Deployment

### Render

Build Command

```bash
pip install -r requirements.txt
```

Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## Future Improvements

- PostgreSQL Support
- Docker Support
- Refresh Tokens
- User Roles
- Pagination
- Search & Filters
- Logging
- CI/CD Pipeline

---

## License

MIT License
