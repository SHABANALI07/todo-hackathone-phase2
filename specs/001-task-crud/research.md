# Phase 0: Research & Technology Decisions

**Feature**: Task CRUD Operations
**Branch**: `001-task-crud`
**Date**: 2026-01-08

## Overview

This document captures technology decisions, best practices research, and architectural patterns for implementing task CRUD operations with JWT authentication and user isolation.

## Technology Stack Decisions

### Backend: FastAPI + SQLModel

**Decision**: Use FastAPI 0.104+ with SQLModel 0.0.14+ for backend API

**Rationale**:
- FastAPI provides automatic OpenAPI documentation, request/response validation via Pydantic
- SQLModel combines SQLAlchemy ORM with Pydantic validation, reducing code duplication
- Native async support for handling concurrent requests efficiently
- Type hints throughout enable better IDE support and catch errors early
- Dependency injection system ideal for JWT authentication middleware

**Alternatives Considered**:
- Django REST Framework: More batteries-included but heavier, less performant for async operations
- Flask: Lighter but lacks native async support and automatic validation

**Best Practices**:
- Use dependency injection for JWT token verification (`Depends()`)
- Implement middleware for authentication that runs before route handlers
- Use Pydantic models for request/response validation
- Leverage SQLModel's dual nature (ORM + validation) to avoid duplicating models
- Use async database sessions for better performance

### Database: Neon PostgreSQL

**Decision**: Neon PostgreSQL (serverless Postgres)

**Rationale**:
- Serverless architecture with auto-scaling and branching support
- Fully compatible with standard PostgreSQL (psycopg2/asyncpg drivers work)
- Connection pooling built-in, ideal for serverless deployments
- Automatic backups and point-in-time recovery
- No manual server management required

**Best Practices**:
- Use asyncpg driver for async connections from FastAPI
- Connection string format: `postgresql+asyncpg://user:pass@host/db`
- Enable SSL mode for production (`?sslmode=require`)
- Use connection pooling via SQLAlchemy's async engine
- Set appropriate pool size limits (min=2, max=10 for typical workloads)

### Authentication: Better Auth with JWT

**Decision**: Better Auth for JWT token generation and verification

**Rationale**:
- Purpose-built for Next.js and modern web applications
- Handles token generation, refresh, and verification
- Supports multiple authentication providers
- Type-safe with TypeScript
- Integrates cleanly with both frontend and backend

**Alternatives Considered**:
- Auth0: Third-party service, adds external dependency
- NextAuth.js: Focused on Next.js, less straightforward backend integration
- Custom JWT: More control but reinventing the wheel, security risks

**Best Practices**:
- Use BETTER_AUTH_SECRET environment variable (minimum 32 characters)
- Set appropriate token expiration (15 minutes access, 7 days refresh)
- Verify JWT signature on every backend request
- Extract user_id from token claims for database filtering
- Return 401 for invalid/missing tokens, 403 for authorization failures
- Use httpOnly cookies for token storage (XSS protection)

### Frontend: Next.js 14 App Router

**Decision**: Next.js 14+ with App Router, TypeScript, and Tailwind CSS

**Rationale**:
- App Router provides server components for better performance
- Built-in routing, server actions, and API route handlers
- TypeScript ensures type safety across frontend
- Tailwind CSS enables rapid, responsive UI development
- React Server Components reduce client-side JavaScript

**Best Practices**:
- Use server components by default, client components only when needed
- Store JWT tokens in httpOnly cookies or secure localStorage
- Implement API client utility with automatic token attachment
- Use React hooks for state management (useState, useEffect)
- Create reusable components (TaskList, TaskForm, TaskItem)
- Implement loading and error states for all async operations

## Authentication & Authorization Pattern

### JWT Token Flow

1. **User Login** (handled by separate auth feature):
   - User submits credentials to Better Auth
   - Better Auth validates and returns JWT access token
   - Frontend stores token securely (httpOnly cookie or localStorage)

2. **API Request Flow**:
   ```
   Frontend Request → Include JWT in Authorization header
   ↓
   FastAPI Middleware → Verify JWT signature
   ↓
   Extract user_id from token claims
   ↓
   Route Handler → Receive user_id via dependency injection
   ↓
   Service Layer → Add user_id filter to all queries
   ↓
   Database → Return only user's data
   ```

3. **Token Verification Logic**:
   ```python
   # Pseudocode
   def verify_token(token: str) -> user_id:
       try:
           payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
           return payload["sub"]  # user_id
       except JWTError:
           raise HTTPException(401, "Invalid token")
   ```

### User Isolation Strategy

**Pattern**: Automatic user_id filtering at service layer

**Implementation**:
- All database queries MUST include `WHERE user_id = ?`
- Service layer methods accept `user_id` as first parameter
- Never trust user_id from request body - always use token claims
- Use SQLModel relationships to enforce foreign key constraints

**Example**:
```python
# Service method signature
async def get_user_tasks(user_id: int, status_filter: str = None) -> List[Task]:
    query = select(Task).where(Task.user_id == user_id)
    if status_filter:
        query = query.where(Task.is_complete == (status_filter == "complete"))
    return await session.execute(query)
```

## API Design Patterns

### RESTful Endpoint Structure

**Decision**: Standard REST conventions for task endpoints

**Endpoints**:
- `GET /api/tasks` - List user's tasks (with optional status filter)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get single task (verify ownership)
- `PUT /api/tasks/{id}` - Update task (verify ownership)
- `DELETE /api/tasks/{id}` - Delete task (verify ownership)
- `PATCH /api/tasks/{id}/toggle` - Toggle completion status (verify ownership)

**Best Practices**:
- Use HTTP status codes correctly: 200 (success), 201 (created), 204 (deleted), 400 (validation), 401 (unauthorized), 403 (forbidden), 404 (not found)
- Return consistent error response format: `{"detail": "error message"}`
- Use query parameters for filtering: `GET /api/tasks?status=complete`
- Include resource in response body for POST/PUT operations
- Use PATCH for partial updates (toggle completion)

### Request/Response Models

**Pattern**: Separate Pydantic models for requests and responses

**Models Needed**:
- `TaskCreate`: title (str), description (Optional[str])
- `TaskUpdate`: title (Optional[str]), description (Optional[str])
- `TaskResponse`: id, title, description, is_complete, created_at, updated_at, user_id
- `TaskList`: tasks (List[TaskResponse]), total_count (int)

**Best Practices**:
- Never expose user_id in create/update requests (always from token)
- Include timestamps in responses for client-side sorting
- Use Optional[] for nullable fields
- Validate string lengths at Pydantic level (min_length, max_length)

## Database Schema Design

### Task Table Structure

**Columns**:
- `id`: SERIAL PRIMARY KEY
- `user_id`: INTEGER NOT NULL FOREIGN KEY REFERENCES users(id)
- `title`: VARCHAR(200) NOT NULL
- `description`: TEXT (nullable)
- `is_complete`: BOOLEAN DEFAULT FALSE
- `created_at`: TIMESTAMP DEFAULT NOW()
- `updated_at`: TIMESTAMP DEFAULT NOW()

**Indexes**:
- Primary: `id`
- Foreign Key: `user_id` (automatically indexed)
- Composite: `(user_id, is_complete)` for filtered queries

**Constraints**:
- `title` length: CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200)
- `description` length: CHECK (LENGTH(description) <= 1000)
- `user_id` NOT NULL and FOREIGN KEY to users table

**Best Practices**:
- Use SERIAL (auto-increment) for id
- Add created_at/updated_at for audit trail
- Index on user_id for fast filtering
- Use composite index (user_id, is_complete) for status filtering
- Set ON DELETE CASCADE for user_id foreign key (tasks deleted when user deleted)

## Error Handling Strategy

### Frontend Error Handling

**Pattern**: Try-catch with user-friendly messages

**Implementation**:
```typescript
try {
    const task = await api.createTask(data);
    // Show success message
} catch (error) {
    if (error.status === 401) {
        // Redirect to login
    } else if (error.status === 400) {
        // Show validation errors
    } else {
        // Generic error message
    }
}
```

**Best Practices**:
- Display validation errors inline on form fields
- Show toast notifications for success/error
- Implement retry logic for network failures
- Redirect to login on 401 errors
- Log errors to console for debugging

### Backend Error Handling

**Pattern**: HTTP exceptions with descriptive messages

**Implementation**:
- Validation errors: 400 with field-specific messages
- Authentication failures: 401 "Invalid or missing token"
- Authorization failures: 403 "Access denied to this resource"
- Not found: 404 "Task not found"
- Server errors: 500 (caught by FastAPI exception handler)

**Best Practices**:
- Use FastAPI's HTTPException for all expected errors
- Let Pydantic handle validation errors (automatic 422 responses)
- Log all 500 errors for debugging
- Never expose internal error details to clients
- Return consistent error format across all endpoints

## Performance Optimization

### Backend Optimizations

**Strategies**:
1. Use async/await throughout for non-blocking I/O
2. Implement database connection pooling
3. Add database indexes on filtered columns
4. Use select() queries instead of loading all columns
5. Implement pagination for task lists (limit/offset)

**Targets**:
- API response time: <200ms p95
- Database query time: <50ms p95
- Handle 100 concurrent requests

### Frontend Optimizations

**Strategies**:
1. Use React Server Components for initial page load
2. Implement optimistic UI updates (toggle completion)
3. Cache task list data with SWR or React Query
4. Lazy load task details on demand
5. Debounce search/filter inputs

**Targets**:
- Initial page load: <2s
- Toggle completion: <1s perceived latency
- Task list render: <100ms for 1000 tasks

## Validation Rules

### Input Validation

**Title**:
- Required field
- Minimum length: 1 character (no empty strings)
- Maximum length: 200 characters
- Trim whitespace before validation
- Reject pure whitespace strings

**Description**:
- Optional field
- Maximum length: 1000 characters
- Allow empty string (treated as null)

**Task ID** (for update/delete/toggle):
- Must be positive integer
- Must exist in database
- Must belong to authenticated user

### Backend Validation

**Implementation**:
```python
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @validator('title')
    def title_not_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be only whitespace')
        return v.strip()
```

### Frontend Validation

**Implementation**:
- Client-side validation before API call
- Show inline errors on form fields
- Disable submit button until validation passes
- Real-time validation on blur/change events

## Testing Strategy

### Backend Testing

**Approach**: pytest with test database

**Test Types**:
1. **Unit Tests** (service layer):
   - Test CRUD operations with mocked database
   - Test user_id filtering logic
   - Test validation rules

2. **Integration Tests** (API endpoints):
   - Test full request/response cycle
   - Test authentication middleware
   - Test authorization (user cannot access others' tasks)
   - Test error responses

**Test Data**:
- Create test users and tasks in setup
- Use fixtures for common test data
- Clean up test data after each test

### Frontend Testing

**Approach**: Jest + React Testing Library

**Test Types**:
1. **Component Tests**:
   - Test TaskForm validation and submission
   - Test TaskList rendering and filtering
   - Test TaskItem toggle completion

2. **Integration Tests**:
   - Test full user flows (create → view → update → delete)
   - Mock API responses
   - Test error handling

## Security Considerations

### OWASP Top 10 Mitigations

1. **Injection Prevention**:
   - Use SQLModel ORM (parameterized queries)
   - Never concatenate user input into SQL

2. **Broken Authentication**:
   - JWT token with signature verification
   - Token expiration enforcement
   - Secure token storage (httpOnly cookies)

3. **Sensitive Data Exposure**:
   - HTTPS only in production
   - Never log JWT tokens
   - Environment variables for secrets

4. **Broken Access Control**:
   - Mandatory user_id filtering on all queries
   - Verify ownership before update/delete
   - 403 for authorization failures

5. **Security Misconfiguration**:
   - Set CORS policies appropriately
   - Disable debug mode in production
   - Use strong BETTER_AUTH_SECRET (32+ chars)

6. **XSS Prevention**:
   - React automatically escapes output
   - Sanitize user input on backend
   - Use httpOnly cookies for tokens

7. **CSRF Prevention**:
   - Use SameSite cookie attribute
   - Implement CSRF tokens for state-changing operations

## Deployment Considerations

### Environment Variables

**Required**:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: JWT signing secret (32+ characters)
- `ALLOWED_ORIGINS`: CORS allowed origins (frontend URL)

**Optional**:
- `LOG_LEVEL`: Logging verbosity (INFO, DEBUG, ERROR)
- `TOKEN_EXPIRY`: JWT expiration time (default: 15m)

### Production Readiness

**Backend**:
- Use production ASGI server (Uvicorn with Gunicorn)
- Enable HTTPS/TLS
- Set up health check endpoint
- Configure logging and monitoring
- Implement rate limiting

**Frontend**:
- Build optimized production bundle
- Enable compression (gzip/brotli)
- Set up CDN for static assets
- Configure caching headers

## Next Steps

After Phase 0 research completion:
1. **Phase 1**: Create detailed data model (data-model.md)
2. **Phase 1**: Generate OpenAPI contract (contracts/tasks-api.yaml)
3. **Phase 1**: Write quickstart guide (quickstart.md)
4. **Phase 2**: Generate implementation tasks (tasks.md via /sp.tasks)

## References

- FastAPI Documentation: https://fastapi.tiangolo.com/
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Better Auth Documentation: https://www.better-auth.com/
- Next.js App Router: https://nextjs.org/docs/app
- Neon PostgreSQL: https://neon.tech/docs/
