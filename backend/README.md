# Notification Service Backend

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```

3. Run the application:
```bash
cd app
python main.py
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

API documentation: `http://localhost:8000/docs`

## Default Admin User

After first run, you can create an admin user via the `/api/auth/register` endpoint with `is_admin: true`.

## API Endpoints

### Authentication
- POST `/api/auth/register` - Register a new user
- POST `/api/auth/login` - Login and get access token

### Notifications
- POST `/api/notifications/` - Create notification (Admin only)
- GET `/api/notifications/` - Get user's notifications
- GET `/api/notifications/unread-count` - Get unread count
- PUT `/api/notifications/{id}/read` - Mark notification as read
- PUT `/api/notifications/mark-all-read` - Mark all as read
- DELETE `/api/notifications/{id}` - Delete notification (Admin only)

### WebSocket
- WS `/ws/{user_id}` - WebSocket connection for real-time updates
