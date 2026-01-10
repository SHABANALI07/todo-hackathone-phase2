# Data Model: Task CRUD Operations

**Feature**: Task CRUD Operations
**Branch**: `001-task-crud`
**Date**: 2026-01-08

## Overview

This document defines the database schema, entity models, and data relationships for the task management system with user isolation.

## Entity Relationship Diagram

```
┌──────────────────┐           ┌──────────────────┐
│      User        │           │      Task        │
├──────────────────┤           ├──────────────────┤
│ id (PK)          │──────────<│ id (PK)          │
│ email            │   1:N     │ user_id (FK)     │
│ password_hash    │           │ title            │
│ created_at       │           │ description      │
│ updated_at       │           │ is_complete      │
└──────────────────┘           │ created_at       │
                               │ updated_at       │
                               └──────────────────┘

Relationship: One User has Many Tasks
Constraint: Tasks MUST have a user_id (NOT NULL)
Cascade: ON DELETE CASCADE (delete tasks when user deleted)
```

## Database Schema

### Task Table

**Table Name**: `tasks`

**Purpose**: Store todo items with user ownership and completion status

**Columns**:

| Column Name   | Data Type      | Constraints                          | Description                          |
|---------------|----------------|--------------------------------------|--------------------------------------|
| id            | SERIAL         | PRIMARY KEY                          | Unique task identifier               |
| user_id       | INTEGER        | NOT NULL, FOREIGN KEY REFERENCES users(id) ON DELETE CASCADE | Owner of the task |
| title         | VARCHAR(200)   | NOT NULL, CHECK(LENGTH(title) >= 1 AND LENGTH(title) <= 200) | Task title (required) |
| description   | TEXT           | NULL, CHECK(description IS NULL OR LENGTH(description) <= 1000) | Optional task details |
| is_complete   | BOOLEAN        | NOT NULL DEFAULT FALSE               | Completion status                    |
| created_at    | TIMESTAMP      | NOT NULL DEFAULT NOW()               | Task creation timestamp              |
| updated_at    | TIMESTAMP      | NOT NULL DEFAULT NOW()               | Last update timestamp                |

**Indexes**:

| Index Name                | Type       | Columns                 | Purpose                              |
|---------------------------|------------|-------------------------|--------------------------------------|
| tasks_pkey                | PRIMARY    | id                      | Primary key (auto-created)           |
| tasks_user_id_idx         | BTREE      | user_id                 | Fast filtering by user               |
| tasks_user_id_status_idx  | BTREE      | user_id, is_complete    | Fast filtered queries (status filter)|
| tasks_created_at_idx      | BTREE      | created_at DESC         | Sorting by creation date             |

**Constraints**:

```sql
-- Primary Key
CONSTRAINT tasks_pkey PRIMARY KEY (id)

-- Foreign Key with cascade delete
CONSTRAINT tasks_user_id_fkey
    FOREIGN KEY (user_id)
    REFERENCES users(id)
    ON DELETE CASCADE

-- Title validation
CONSTRAINT tasks_title_check
    CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200)

-- Description validation
CONSTRAINT tasks_description_check
    CHECK (description IS NULL OR LENGTH(description) <= 1000)

-- Not null constraints
CONSTRAINT tasks_user_id_not_null CHECK (user_id IS NOT NULL)
CONSTRAINT tasks_title_not_null CHECK (title IS NOT NULL)
CONSTRAINT tasks_is_complete_not_null CHECK (is_complete IS NOT NULL)
```

**SQL DDL**:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT tasks_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT tasks_title_check
        CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200),

    CONSTRAINT tasks_description_check
        CHECK (description IS NULL OR LENGTH(description) <= 1000)
);

-- Indexes for performance
CREATE INDEX tasks_user_id_idx ON tasks(user_id);
CREATE INDEX tasks_user_id_status_idx ON tasks(user_id, is_complete);
CREATE INDEX tasks_created_at_idx ON tasks(created_at DESC);

-- Trigger for updated_at timestamp
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

### User Table (Reference)

**Note**: User table is defined in the separate authentication feature. Included here for reference.

**Table Name**: `users`

**Columns** (minimal schema for task reference):

| Column Name   | Data Type      | Constraints        | Description              |
|---------------|----------------|--------------------|--------------------------|
| id            | SERIAL         | PRIMARY KEY        | Unique user identifier   |
| email         | VARCHAR(255)   | UNIQUE, NOT NULL   | User email (login)       |
| password_hash | VARCHAR(255)   | NOT NULL           | Hashed password          |
| created_at    | TIMESTAMP      | NOT NULL           | Account creation time    |
| updated_at    | TIMESTAMP      | NOT NULL           | Last update time         |

## Backend Models (SQLModel/Pydantic)

### Task Model (ORM)

**File**: `backend/src/models/task.py`

**Purpose**: SQLModel class for database operations and validation

```python
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (auto-generated)
        user_id: Owner user ID (required, foreign key)
        title: Task title, 1-200 characters (required)
        description: Optional task details, max 1000 characters
        is_complete: Completion status (default: False)
        created_at: Creation timestamp (auto-generated)
        updated_at: Last update timestamp (auto-updated)
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_complete: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships (if needed for joins)
    # user: Optional["User"] = Relationship(back_populates="tasks")
```

### Request Models (Pydantic)

**Purpose**: Validate incoming API requests

```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class TaskCreate(BaseModel):
    """Request model for creating a new task"""
    title: str = Field(min_length=1, max_length=200, description="Task title (required)")
    description: Optional[str] = Field(None, max_length=1000, description="Task description (optional)")

    @validator('title')
    def title_not_whitespace(cls, v):
        """Ensure title is not only whitespace"""
        if not v.strip():
            raise ValueError('Title cannot be only whitespace')
        return v.strip()

    @validator('description')
    def clean_description(cls, v):
        """Trim description whitespace"""
        if v:
            return v.strip() if v.strip() else None
        return None

class TaskUpdate(BaseModel):
    """Request model for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @validator('title')
    def title_not_whitespace(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be only whitespace')
        return v.strip() if v else None

    @validator('description')
    def clean_description(cls, v):
        if v:
            return v.strip() if v.strip() else None
        return None
```

### Response Models (Pydantic)

**Purpose**: Structure API responses

```python
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TaskResponse(BaseModel):
    """Response model for a single task"""
    id: int
    title: str
    description: Optional[str]
    is_complete: bool
    created_at: datetime
    updated_at: datetime
    user_id: int  # Included for reference, but never editable via API

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel conversion

class TaskListResponse(BaseModel):
    """Response model for task list"""
    tasks: List[TaskResponse]
    total_count: int
    filtered_count: int  # Count after applying status filter
```

## Frontend Models (TypeScript)

### Task Interface

**File**: `frontend/src/lib/types.ts`

**Purpose**: TypeScript types for frontend data handling

```typescript
/**
 * Task entity representing a todo item
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_complete: boolean;
  created_at: string;  // ISO 8601 datetime string
  updated_at: string;  // ISO 8601 datetime string
  user_id: number;
}

/**
 * Request payload for creating a new task
 */
export interface TaskCreateRequest {
  title: string;
  description?: string | null;
}

/**
 * Request payload for updating an existing task
 */
export interface TaskUpdateRequest {
  title?: string;
  description?: string | null;
}

/**
 * Response from task list endpoint
 */
export interface TaskListResponse {
  tasks: Task[];
  total_count: number;
  filtered_count: number;
}

/**
 * Status filter options
 */
export type TaskStatusFilter = 'all' | 'complete' | 'incomplete';

/**
 * API error response structure
 */
export interface ApiError {
  detail: string;
}
```

## Data Validation Rules

### Title Field

**Validation**:
- Required: Yes
- Type: String
- Min Length: 1 character
- Max Length: 200 characters
- Trim: Yes (remove leading/trailing whitespace)
- Reject: Pure whitespace strings

**Error Messages**:
- Empty: "Title is required"
- Too short: "Title must be at least 1 character"
- Too long: "Title cannot exceed 200 characters"
- Whitespace: "Title cannot be only whitespace"

### Description Field

**Validation**:
- Required: No
- Type: String or null
- Min Length: None
- Max Length: 1000 characters
- Trim: Yes
- Empty String Handling: Convert to null

**Error Messages**:
- Too long: "Description cannot exceed 1000 characters"

### ID Field (for operations)

**Validation**:
- Type: Positive integer
- Existence: Must exist in database
- Ownership: Must belong to authenticated user

**Error Messages**:
- Invalid format: "Invalid task ID"
- Not found: "Task not found"
- Unauthorized: "Access denied to this task"

## Data Access Patterns

### Create Task

**Input**: TaskCreate (title, description), user_id (from JWT)
**Process**:
1. Validate input (Pydantic automatic)
2. Create Task instance with user_id
3. Insert into database
4. Return TaskResponse

**SQL**:
```sql
INSERT INTO tasks (user_id, title, description, is_complete, created_at, updated_at)
VALUES ($1, $2, $3, FALSE, NOW(), NOW())
RETURNING *;
```

### Get Task List

**Input**: user_id (from JWT), status_filter (optional)
**Process**:
1. Query tasks WHERE user_id = $1
2. Apply status filter if provided
3. Order by created_at DESC
4. Return TaskListResponse

**SQL**:
```sql
-- Without filter
SELECT * FROM tasks
WHERE user_id = $1
ORDER BY created_at DESC;

-- With complete filter
SELECT * FROM tasks
WHERE user_id = $1 AND is_complete = TRUE
ORDER BY created_at DESC;

-- With incomplete filter
SELECT * FROM tasks
WHERE user_id = $1 AND is_complete = FALSE
ORDER BY created_at DESC;
```

### Get Single Task

**Input**: task_id, user_id (from JWT)
**Process**:
1. Query task WHERE id = $1 AND user_id = $2
2. If not found, return 404
3. Return TaskResponse

**SQL**:
```sql
SELECT * FROM tasks
WHERE id = $1 AND user_id = $2;
```

### Update Task

**Input**: task_id, TaskUpdate (title, description), user_id (from JWT)
**Process**:
1. Verify ownership (WHERE id = $1 AND user_id = $2)
2. If not found/unauthorized, return 403/404
3. Update fields (only provided fields)
4. Trigger updates updated_at
5. Return TaskResponse

**SQL**:
```sql
UPDATE tasks
SET
    title = COALESCE($1, title),
    description = COALESCE($2, description),
    updated_at = NOW()
WHERE id = $3 AND user_id = $4
RETURNING *;
```

### Delete Task

**Input**: task_id, user_id (from JWT)
**Process**:
1. Verify ownership (WHERE id = $1 AND user_id = $2)
2. If not found/unauthorized, return 403/404
3. Delete task
4. Return 204 No Content

**SQL**:
```sql
DELETE FROM tasks
WHERE id = $1 AND user_id = $2;
```

### Toggle Completion

**Input**: task_id, user_id (from JWT)
**Process**:
1. Verify ownership
2. Toggle is_complete field
3. Update updated_at
4. Return TaskResponse

**SQL**:
```sql
UPDATE tasks
SET
    is_complete = NOT is_complete,
    updated_at = NOW()
WHERE id = $1 AND user_id = $2
RETURNING *;
```

## Performance Considerations

### Index Usage

**Query**: List tasks by user
```sql
SELECT * FROM tasks WHERE user_id = $1;
-- Uses: tasks_user_id_idx
```

**Query**: List complete tasks by user
```sql
SELECT * FROM tasks WHERE user_id = $1 AND is_complete = TRUE;
-- Uses: tasks_user_id_status_idx (composite index)
```

**Query**: Recent tasks first
```sql
SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC;
-- Uses: tasks_user_id_idx + tasks_created_at_idx
```

### Optimization Notes

- Composite index (user_id, is_complete) covers both WHERE clauses efficiently
- created_at index DESC matches common sort order (newest first)
- Foreign key index on user_id enables fast joins if needed
- SERIAL primary key ensures sequential IDs and fast lookups

## Migration Strategy

**Initial Migration** (create tables):
```sql
-- Run as part of database setup
-- File: backend/migrations/001_create_tasks_table.sql

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT tasks_user_id_fkey
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CONSTRAINT tasks_title_check
        CHECK (LENGTH(title) >= 1 AND LENGTH(title) <= 200),

    CONSTRAINT tasks_description_check
        CHECK (description IS NULL OR LENGTH(description) <= 1000)
);

CREATE INDEX tasks_user_id_idx ON tasks(user_id);
CREATE INDEX tasks_user_id_status_idx ON tasks(user_id, is_complete);
CREATE INDEX tasks_created_at_idx ON tasks(created_at DESC);

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

**Rollback Migration**:
```sql
-- File: backend/migrations/001_create_tasks_table_down.sql

DROP TRIGGER IF EXISTS update_tasks_updated_at ON tasks;
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP INDEX IF EXISTS tasks_created_at_idx;
DROP INDEX IF EXISTS tasks_user_id_status_idx;
DROP INDEX IF EXISTS tasks_user_id_idx;
DROP TABLE IF EXISTS tasks;
```

## Testing Data

### Sample Data for Development

```sql
-- Assuming user with id=1 exists
INSERT INTO tasks (user_id, title, description, is_complete, created_at, updated_at) VALUES
(1, 'Complete project proposal', 'Draft and submit the Q1 project proposal document', FALSE, NOW() - INTERVAL '2 days', NOW() - INTERVAL '2 days'),
(1, 'Review pull requests', NULL, TRUE, NOW() - INTERVAL '1 day', NOW()),
(1, 'Schedule team meeting', 'Book conference room for Monday standup', FALSE, NOW(), NOW()),
(1, 'Update documentation', 'Add API endpoints to developer guide', FALSE, NOW() - INTERVAL '3 hours', NOW() - INTERVAL '1 hour'),
(1, 'Fix bug #123', 'Login form validation error on mobile', TRUE, NOW() - INTERVAL '5 days', NOW() - INTERVAL '4 days');
```

## Next Steps

- **Phase 1**: Generate API contracts (contracts/tasks-api.yaml)
- **Phase 1**: Create quickstart guide (quickstart.md)
- **Phase 2**: Generate implementation tasks (tasks.md)
