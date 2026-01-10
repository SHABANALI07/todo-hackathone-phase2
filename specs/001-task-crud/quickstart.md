# Quickstart Guide: Task CRUD Operations

**Feature**: Task CRUD Operations
**Branch**: `001-task-crud`
**Date**: 2026-01-08

## Overview

This guide provides step-by-step instructions for setting up, developing, and testing the Task CRUD Operations feature with authentication and user isolation.

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed
- **Node.js 18+** and npm/yarn installed
- **Neon PostgreSQL database** provisioned and accessible
- **Better Auth** configured with BETTER_AUTH_SECRET
- **Git** for version control
- **Code editor** (VS Code recommended)

## Project Structure

```
todo-hackathon-phase2/
├── backend/               # FastAPI backend
│   ├── src/
│   │   ├── models/       # SQLModel entities
│   │   ├── services/     # Business logic
│   │   ├── api/          # API routes
│   │   ├── middleware/   # JWT authentication
│   │   └── main.py       # App entry point
│   ├── tests/            # Backend tests
│   └── requirements.txt  # Python dependencies
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── lib/          # Utilities and API client
│   ├── tests/            # Frontend tests
│   └── package.json      # Node dependencies
└── specs/001-task-crud/  # Feature documentation
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md (this file)
    └── contracts/
        └── tasks-api.yaml
```

## Setup Instructions

### 1. Environment Configuration

#### Backend Environment Variables

Create `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@your-neon-host/dbname?sslmode=require

# Authentication
BETTER_AUTH_SECRET=your-32-character-secret-here-change-this

# API Configuration
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Application
LOG_LEVEL=INFO
DEBUG=False
```

**Generate BETTER_AUTH_SECRET**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Frontend Environment Variables

Create `frontend/.env.local`:

```bash
# API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=same-secret-as-backend
BETTER_AUTH_URL=http://localhost:8000/api/auth
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt** should include:
```
fastapi==0.104.1
sqlmodel==0.0.14
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
asyncpg==0.29.0
```

#### Database Migration

Run the SQL migration to create the tasks table:

```bash
# Connect to your Neon database
psql $DATABASE_URL

# Or run migration script
psql $DATABASE_URL -f specs/001-task-crud/migrations/001_create_tasks_table.sql
```

Migration SQL (from data-model.md):
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT tasks_user_id_fkey
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT tasks_title_check
        CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200),
    CONSTRAINT tasks_description_check
        CHECK (description IS NULL OR LENGTH(description) <= 1000)
);

CREATE INDEX tasks_user_id_idx ON tasks(user_id);
CREATE INDEX tasks_user_id_status_idx ON tasks(user_id, is_complete);
CREATE INDEX tasks_created_at_idx ON tasks(created_at DESC);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

#### Run Backend Server

```bash
# Development mode with auto-reload
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Or using script
python -m src.main
```

Verify backend is running:
```bash
curl http://localhost:8000/docs
# Should show FastAPI Swagger UI
```

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend

# Install packages
npm install
# or
yarn install
```

**package.json** should include:
```json
{
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "typescript": "^5.3.0",
    "tailwindcss": "^3.3.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "eslint": "^8.0.0",
    "eslint-config-next": "^14.0.0"
  }
}
```

#### Run Frontend Development Server

```bash
npm run dev
# or
yarn dev
```

Visit http://localhost:3000 to see the application.

### 4. Verify Setup

#### Health Check

Backend health:
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

Frontend health:
```bash
curl http://localhost:3000
# Expected: HTML response
```

## Development Workflow

### 1. Create a Task (API Example)

**Prerequisite**: Obtain JWT token from authentication endpoint

```bash
# Login to get token (assuming auth feature exists)
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}' \
  | jq -r '.access_token')

# Create a task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal",
    "description": "Draft and submit the Q1 project proposal"
  }'

# Expected response:
# {
#   "id": 1,
#   "title": "Complete project proposal",
#   "description": "Draft and submit the Q1 project proposal",
#   "is_complete": false,
#   "created_at": "2026-01-08T10:30:00Z",
#   "updated_at": "2026-01-08T10:30:00Z",
#   "user_id": 42
# }
```

### 2. List Tasks

```bash
# List all tasks
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"

# List only complete tasks
curl "http://localhost:8000/api/tasks?status=complete" \
  -H "Authorization: Bearer $TOKEN"

# List only incomplete tasks
curl "http://localhost:8000/api/tasks?status=incomplete" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. Get Single Task

```bash
curl http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

### 4. Update Task

```bash
curl -X PUT http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project proposal by Friday",
    "description": "Draft, review, and submit by EOD Friday"
  }'
```

### 5. Toggle Completion

```bash
curl -X PATCH http://localhost:8000/api/tasks/1/toggle \
  -H "Authorization: Bearer $TOKEN"
```

### 6. Delete Task

```bash
curl -X DELETE http://localhost:8000/api/tasks/1 \
  -H "Authorization: Bearer $TOKEN"
```

## Frontend Usage

### Task List Page

Navigate to http://localhost:3000/tasks

**Features**:
- View all your tasks
- Filter by status (All / Complete / Incomplete)
- See creation dates
- Click task to edit
- Toggle completion with checkbox
- Delete button for each task

### Create Task Page

Navigate to http://localhost:3000/tasks/new

**Features**:
- Title input (required, 1-200 chars)
- Description textarea (optional, max 1000 chars)
- Real-time validation
- Submit button (disabled until valid)

### Edit Task Page

Navigate to http://localhost:3000/tasks/[id]

**Features**:
- Pre-filled form with existing task data
- Update title and/or description
- Save changes button
- Cancel button to return to list

## Testing

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_task_api.py

# Run specific test
pytest tests/test_task_api.py::test_create_task
```

**Test Coverage Requirements**:
- Service layer: 100% coverage
- API endpoints: 100% coverage
- Models: 80%+ coverage

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test
# or
yarn test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test TaskList.test.tsx

# Run in watch mode
npm test -- --watch
```

## Common Issues & Troubleshooting

### Issue: Database Connection Error

**Symptom**: `asyncpg.exceptions.InvalidCatalogNameError`

**Solution**:
1. Verify DATABASE_URL in .env
2. Ensure Neon database exists and is accessible
3. Check network connectivity to Neon
4. Verify SSL mode is set (`?sslmode=require`)

### Issue: JWT Token Invalid

**Symptom**: `401 Unauthorized` on all requests

**Solution**:
1. Verify BETTER_AUTH_SECRET matches between frontend and backend
2. Check token expiration (default 15 minutes)
3. Ensure token is included in Authorization header: `Bearer <token>`
4. Re-login to get fresh token

### Issue: User Cannot See Tasks

**Symptom**: Empty task list despite creating tasks

**Solution**:
1. Verify user_id from JWT token matches task user_id
2. Check database: `SELECT * FROM tasks WHERE user_id = ?`
3. Ensure middleware extracts user_id from token correctly
4. Check CORS settings if frontend/backend on different domains

### Issue: Validation Errors

**Symptom**: `400 Bad Request` with validation error

**Solution**:
1. Check title length (1-200 characters)
2. Check description length (max 1000 characters)
3. Ensure title is not only whitespace
4. Verify JSON format is correct

### Issue: Cannot Update/Delete Other User's Task

**Symptom**: `403 Forbidden`

**Solution**:
This is expected behavior! Users can only modify their own tasks. Verify you're logged in as the correct user.

## Performance Benchmarks

### Expected Performance

**Backend API**:
- List tasks (100 tasks): < 100ms
- Create task: < 50ms
- Update task: < 50ms
- Delete task: < 30ms
- Toggle completion: < 30ms

**Frontend**:
- Initial page load: < 2s
- Task list render: < 100ms
- Toggle completion (perceived): < 1s
- Form submission: < 500ms

### Load Testing

Using `locust` or `ab` (Apache Bench):

```bash
# Install locust
pip install locust

# Run load test
locust -f tests/load_test.py --host http://localhost:8000

# Or use Apache Bench
ab -n 1000 -c 10 -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/tasks
```

## Security Checklist

Before deployment, verify:

- [ ] BETTER_AUTH_SECRET is strong (32+ characters)
- [ ] DATABASE_URL does not contain plain password in logs
- [ ] HTTPS enabled in production
- [ ] CORS restricted to specific origins (not *)
- [ ] JWT token expiration set appropriately
- [ ] User isolation tested (cannot access other users' tasks)
- [ ] Input validation working (XSS prevention)
- [ ] SQL injection prevented (ORM parameterized queries)
- [ ] Error messages don't expose sensitive information
- [ ] Rate limiting configured

## Next Steps

After completing local development:

1. **Write Tests**: Implement unit and integration tests (see tasks.md)
2. **Code Review**: Have plan and implementation reviewed
3. **Deploy to Staging**: Test in production-like environment
4. **Performance Testing**: Run load tests, optimize queries
5. **Security Audit**: Penetration testing, code review
6. **Deploy to Production**: Follow deployment checklist

## Additional Resources

### Documentation
- API Contract: `specs/001-task-crud/contracts/tasks-api.yaml`
- Data Model: `specs/001-task-crud/data-model.md`
- Research: `specs/001-task-crud/research.md`
- Implementation Plan: `specs/001-task-crud/plan.md`

### External References
- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Next.js App Router: https://nextjs.org/docs/app
- Better Auth: https://www.better-auth.com/
- Neon PostgreSQL: https://neon.tech/docs/

### Support

For issues or questions:
1. Check this quickstart guide
2. Review spec and plan documents
3. Check application logs
4. Consult project constitution (.specify/memory/constitution.md)

## Development Commands Reference

**Backend**:
```bash
# Start server
uvicorn src.main:app --reload --port 8000

# Run tests
pytest

# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

**Frontend**:
```bash
# Start dev server
npm run dev

# Build production
npm run build

# Run production
npm start

# Run tests
npm test

# Lint
npm run lint

# Format
npm run format
```

**Database**:
```bash
# Connect to Neon
psql $DATABASE_URL

# Run migration
psql $DATABASE_URL -f migration.sql

# Check tables
psql $DATABASE_URL -c "\dt"

# View tasks
psql $DATABASE_URL -c "SELECT * FROM tasks;"
```

## Conclusion

You should now have a fully functional Task CRUD Operations feature with authentication and user isolation. The API endpoints are documented in the OpenAPI spec, and the frontend provides a complete user interface for task management.

For implementation details, refer to the tasks.md file (generated via `/sp.tasks` command).
