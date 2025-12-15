# Notification Service

A role-based notification messenger system built with FastAPI (backend) and Next.js (frontend). The system supports real-time notifications, offline message persistence, and read/unread tracking.

## Features

### Core Features
- **Role-Based Access Control**: Admin and User roles
- **Real-Time Notifications**: WebSocket support for instant updates
- **Offline Message Persistence**: Users receive notifications when they log in, even if sent while offline
- **Read/Unread Tracking**: Mark notifications as read individually or all at once
- **User Authentication**: JWT-based authentication system
- **Notification Management**: Create, read, and delete notifications

### Admin Features
- Send notifications to all users
- View notification history
- Delete notifications

### User Features
- View all notifications
- Filter by unread notifications
- Mark notifications as read
- Mark all notifications as read
- See unread count badge
- Real-time notification updates via WebSocket

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Database
- **JWT**: Authentication
- **WebSockets**: Real-time communication
- **Pydantic**: Data validation

### Frontend
- **Next.js 14**: React framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client
- **WebSocket API**: Real-time updates

## Project Structure

```
notification_service/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database models and setup
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── auth.py              # Authentication utilities
│   │   ├── routes_auth.py       # Authentication routes
│   │   └── routes_notifications.py  # Notification routes
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── README.md               # Backend documentation
│
└── frontend/
    ├── app/
    │   ├── page.tsx            # Home page (redirects)
    │   ├── layout.tsx          # Root layout with AuthProvider
    │   ├── login/              # Login page
    │   ├── register/           # Register page
    │   ├── dashboard/          # User dashboard
    │   └── admin/              # Admin dashboard
    ├── components/
    │   ├── NotificationList.tsx    # Notification list component
    │   └── NotificationForm.tsx    # Admin notification form
    ├── contexts/
    │   └── AuthContext.tsx     # Authentication context
    ├── lib/
    │   └── api.ts              # API client
    └── package.json            # Node dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Run the application:
```bash
cd app
python main.py
```

Or use uvicorn:
```bash
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Usage

### Creating an Admin User

1. Go to `http://localhost:3000/register`
2. Fill in the registration form
3. Check "Register as Admin" checkbox
4. Click "Register"

### Creating a Regular User

1. Go to `http://localhost:3000/register`
2. Fill in the registration form
3. Leave "Register as Admin" unchecked
4. Click "Register"

### Admin Dashboard

- **Send Notifications**: Use the form to create and send notifications to all users
- **View Notifications**: See all notifications and their status
- **Real-time Updates**: Automatically receive new notifications

### User Dashboard

- **View Notifications**: See all your notifications
- **Filter Unread**: Toggle to show only unread notifications
- **Mark as Read**: Click to mark individual notifications as read
- **Mark All as Read**: Mark all notifications as read at once
- **Unread Count Badge**: See how many unread notifications you have
- **Real-time Updates**: Automatically receive new notifications

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token

### Notifications
- `POST /api/notifications/` - Create notification (Admin only)
- `GET /api/notifications/` - Get user's notifications
- `GET /api/notifications/?unread_only=true` - Get only unread notifications
- `GET /api/notifications/unread-count` - Get unread count
- `PUT /api/notifications/{id}/read` - Mark notification as read
- `PUT /api/notifications/mark-all-read` - Mark all as read
- `DELETE /api/notifications/{id}` - Delete notification (Admin only)

### WebSocket
- `WS /ws/{user_id}` - WebSocket connection for real-time updates

## Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `hashed_password`: Bcrypt hashed password
- `is_admin`: Boolean flag for admin role
- `created_at`: Timestamp

### Notifications
- `id`: Primary key
- `title`: Notification title
- `message`: Notification message
- `created_by`: Foreign key to User
- `created_at`: Timestamp

### NotificationStatus
- `id`: Primary key
- `notification_id`: Foreign key to Notification
- `user_id`: Foreign key to User
- `is_read`: Boolean flag
- `read_at`: Timestamp (nullable)

## How It Works

### Notification Flow

1. **Admin Creates Notification**:
   - Admin submits notification through the form
   - Backend creates a Notification record
   - Backend creates NotificationStatus records for all users
   - Backend broadcasts via WebSocket to all connected users

2. **User Receives Notification**:
   - If online: WebSocket pushes notification instantly
   - If offline: Notification waits in database
   - When user logs in: All unread notifications are fetched

3. **User Marks as Read**:
   - User clicks "Mark as Read"
   - Frontend calls API to update NotificationStatus
   - Backend updates the database
   - Frontend refreshes the list

### Real-Time Updates

- WebSocket connection established on dashboard mount
- Server broadcasts to all connected users when new notification is created
- Clients automatically fetch new notifications when WebSocket message received
- Connection managed per user session

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access**: Admin-only endpoints protected
- **CORS Configuration**: Restricted to localhost in development

## Future Enhancements

- Email notifications
- Push notifications
- Notification categories/tags
- User preferences for notification types
- Notification scheduling
- Rich text editor for messages
- File attachments
- User groups/teams
- Notification analytics
- Read receipts
- Notification search
- Export notifications

## License

MIT

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
