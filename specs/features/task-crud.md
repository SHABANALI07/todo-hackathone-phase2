# Feature: Task CRUD Operations

## User Stories
- Logged-in user new task create kare (title required, description optional)
- User apne tasks list dekhe (status, created date ke saath)
- User task update kare
- User task delete kare
- User task complete toggle kare

## Acceptance Criteria
- Create: Title 1-200 chars, description max 1000, user_id se associate
- List: Only current user's tasks, filter by status
- Update/Delete/Complete: Invalid ID → error, only own task
- All operations JWT verified – no token → 401

## Technical
- API: GET/POST/PUT/DELETE/PATCH /api/tasks
- Database: tasks table with user_id
- Frontend: Forms and list page
- Use agent for task operations (reusable skill)
