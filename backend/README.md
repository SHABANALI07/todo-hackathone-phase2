# Todo App - Backend API

FastAPI backend for Task CRUD Operations with JWT authentication and user isolation.

## Features

- ✅ Complete CRUD operations for tasks
- ✅ JWT-based authentication
- ✅ User isolation (strict filtering by user_id)
- ✅ PostgreSQL database with SQLModel ORM
- ✅ Async/await for high performance
- ✅ Automatic API documentation (Swagger/OpenAPI)
- ✅ CORS middleware for frontend integration

## Tech Stack

- **Python 3.11+**
- **FastAPI 0.104+** - Modern async web framework
- **SQLModel 0.0.14+** - ORM with Pydantic validation
- **Neon PostgreSQL** - Cloud-hosted database
- **python-jose** - JWT token handling
- **asyncpg** - Async PostgreSQL driver

## Setup

### 1. Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DATABASE_URL=postgresql+asyncpg://user:password@your-neon-host/dbname?sslmode=require
BETTER_AUTH_SECRET=your-32-character-secret-here
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
LOG_LEVEL=INFO
DEBUG=False
```

**Generate BETTER_AUTH_SECRET:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Database Migration

Run the SQL migration to create the tasks table:

```bash
psql $DATABASE_URL -f migrations/001_create_tasks_table.sql
```

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python module
python -m src.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check

```bash
GET /health
```

### Tasks

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

#### Create Task
```bash
POST /api/tasks
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Complete project proposal",
  "description": "Draft and submit the Q1 project proposal"
}
```

#### Get Task List
```bash
GET /api/tasks?status=all
Authorization: Bearer <token>
```

Query parameters:
- `status`: Filter by status (`all`, `complete`, `incomplete`)

#### Get Single Task
```bash
GET /api/tasks/{id}
Authorization: Bearer <token>
```

#### Update Task
```bash
PUT /api/tasks/{id}
Content-Type: application/json
Authorization: Bearer <token>

{
  "title": "Updated title",
  "description": "Updated description"
}
```

#### Delete Task
```bash
DELETE /api/tasks/{id}
Authorization: Bearer <token>
```

#### Toggle Completion
```bash
PATCH /api/tasks/{id}/toggle
Authorization: Bearer <token>
```

## Project Structure

```
backend/
├── src/
│   ├── models/
│   │   ├── task.py          # Task SQLModel
│   │   └── schemas.py       # Pydantic request/response models
│   ├── services/
│   │   ├── auth.py          # JWT verification
│   │   └── task_service.py  # Task CRUD business logic
│   ├── api/
│   │   └── tasks.py         # FastAPI route handlers
│   ├── middleware/
│   │   └── auth.py          # JWT authentication middleware
│   ├── database.py          # Database connection
│   └── main.py              # FastAPI app initialization
├── migrations/
│   └── 001_create_tasks_table.sql
├── requirements.txt
├── .env.example
└── README.md
```

## Security

- ✅ JWT signature verification on all endpoints
- ✅ User isolation: all database queries filter by `user_id`
- ✅ Input validation via Pydantic
- ✅ SQL injection prevention (parameterized queries)
- ✅ CORS restricted to allowed origins
- ✅ HTTPS required in production

## Development

### Code Style

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

### Database

```bash
# Connect to Neon database
psql $DATABASE_URL

# View tasks table
psql $DATABASE_URL -c "SELECT * FROM tasks;"

# Check indexes
psql $DATABASE_URL -c "\d tasks"
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in `.env`
2. Use strong `BETTER_AUTH_SECRET` (32+ characters)
3. Configure HTTPS/TLS
4. Use production ASGI server (Gunicorn + Uvicorn)
5. Set up monitoring and logging

## Troubleshooting

### Database Connection Error

Ensure:
- DATABASE_URL is correct
- Neon database exists and is accessible
- SSL mode is set: `?sslmode=require`

### Authentication Errors

Verify:
- BETTER_AUTH_SECRET matches between frontend and backend
- Token is included in Authorization header: `Bearer <token>`
- Token has not expired (default: 15 minutes)

## License

MIT License
