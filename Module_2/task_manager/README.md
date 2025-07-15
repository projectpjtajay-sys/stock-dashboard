# Task Manager with Real-time Notifications

A FastAPI-based Task Manager application that allows users to create, update, delete, and view tasks with real-time WebSocket notifications and JWT authentication.

## Features

- User Authentication (Login via JWT)
- Task CRUD (Create, Read, Update, Delete)
- Real-time notifications using WebSocket:
  - On Task Create / Update / Delete
  - Personal or Broadcast messages
- Secure password hashing (bcrypt)
- WebSocket endpoint for live updates

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy
- **Database**: SQLite (can be switched to PostgreSQL/MySQL)
- **Auth**: OAuth2PasswordBearer (JWT tokens)
- **Real-time**: WebSocket (FastAPI native)
- **Password hashing**: passlib (bcrypt)

## Project Structure

```plaintext
task_manager/
├── src/
│   ├── auth/                # Login logic
│   ├── database/            # DB engine & session
│   ├── models/              # SQLAlchemy models
│   ├── notifications/       # WebSocket logic
│   ├── schemas/             # Pydantic schemas
│   ├── tasks/               # Task CRUD service & routes
│   ├── utils/               # Utility functions (JWT, hashing)
│   └── main.py              # FastAPI entry point
├── static/
│   └── websocket_client.html  # Frontend to test WebSocket
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```


### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
uvicorn src.main:app --reload
```

Visit the app documentation at:  
[http://localhost:8000/docs](http://localhost:8000/docs)

## Sample User for Testing

| Username | Password |
|----------|----------|
| ajay     | ajay     |

## WebSocket Testing

Open the WebSocket test page:  
[http://localhost:8000/static/websocket_client.html](http://localhost:8000/static/websocket_test.html)

- Enter your user ID (e.g., `ajay`, matching the username used in authentication)
- Click **Connect**
- Use the API documentation (Swagger) at `http://localhost:8000/docs` to:
  - Send a personal message: `POST /notifications/personal`
  - Send a broadcast message: `POST /notifications/broadcast`
- Watch messages appear in real-time

## API Endpoints

### Auth

- `POST /auth/register` → Register a new user
- `POST /auth/login` → Returns JWT token


### Tasks (Protected)

- `POST /tasks/` → Create a new task
- `GET /tasks/all` → Retrieve all tasks
- `PUT /tasks/{task_id}` → Update a task
- `DELETE /tasks/{task_id}` → Delete a task

### Notifications

- `POST /notifications/personal` → Send personal message
- `POST /notifications/broadcast` → Send message to all users