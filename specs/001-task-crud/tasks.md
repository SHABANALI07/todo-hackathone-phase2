# Tasks: Task CRUD Operations

**Input**: Design documents from `/specs/001-task-crud/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT requested in the feature specification, so test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- Paths are relative to repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend directory structure (backend/src/models/, backend/src/services/, backend/src/api/, backend/src/middleware/)
- [X] T002 Create frontend directory structure (frontend/src/app/, frontend/src/components/, frontend/src/lib/)
- [X] T003 [P] Initialize backend Python project with requirements.txt (FastAPI 0.104+, SQLModel 0.0.14+, Pydantic 2.x, python-jose, asyncpg)
- [X] T004 [P] Initialize frontend Node project with package.json (Next.js 14+, TypeScript 5.x, Tailwind CSS 3.x, React 18+)
- [X] T005 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS
- [X] T006 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 Create database migration script backend/migrations/001_create_tasks_table.sql (tasks table with user_id FK, indexes, triggers)
- [ ] T008 Run database migration to create tasks table in Neon PostgreSQL
- [X] T009 [P] Implement database connection in backend/src/database.py (SQLModel async engine, session management)
- [X] T010 [P] Create Task model in backend/src/models/task.py (SQLModel with user_id FK, title, description, is_complete, timestamps)
- [X] T011 [P] Create Pydantic request models in backend/src/models/schemas.py (TaskCreate, TaskUpdate)
- [X] T012 [P] Create Pydantic response models in backend/src/models/schemas.py (TaskResponse, TaskListResponse)
- [X] T013 Implement JWT verification utility in backend/src/services/auth.py (decode token, extract user_id, handle errors)
- [X] T014 Implement authentication middleware in backend/src/middleware/auth.py (verify JWT, inject user_id into request state, return 401 on failure)
- [X] T015 Create FastAPI app instance in backend/src/main.py (CORS middleware, authentication middleware, route registration)
- [X] T016 [P] Create TypeScript types in frontend/src/lib/types.ts (Task, TaskCreateRequest, TaskUpdateRequest, TaskListResponse, TaskStatusFilter)
- [X] T017 [P] Implement API client utility in frontend/src/lib/api.ts (fetch wrapper with JWT header injection, error handling)
- [X] T018 [P] Create Tailwind CSS configuration in frontend/tailwind.config.js (custom theme, responsive breakpoints)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create New Task (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to create tasks with title and optional description

**Independent Test**: Login, create task with title, verify it appears in task list and is associated with user account

### Implementation for User Story 1

- [ ] T019 [P] [US1] Implement TaskService.create_task method in backend/src/services/task_service.py (accept user_id and TaskCreate, insert into DB, return TaskResponse)
- [ ] T020 [US1] Implement POST /api/tasks endpoint in backend/src/api/tasks.py (extract user_id from middleware, call TaskService.create_task, return 201 with TaskResponse)
- [ ] T021 [P] [US1] Create TaskForm component in frontend/src/components/TaskForm.tsx (title input, description textarea, validation, submit handler)
- [ ] T022 [US1] Create task creation page in frontend/src/app/tasks/new/page.tsx (render TaskForm, call API on submit, redirect to list on success)
- [ ] T023 [US1] Add form validation to TaskForm (title required 1-200 chars, description max 1000 chars, display inline errors)
- [ ] T024 [US1] Add error handling to task creation (display validation errors, handle 401 redirect to login, show success message)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Task List (Priority: P2)

**Goal**: Allow authenticated users to view their tasks with status filtering and display details

**Independent Test**: Login with account that has tasks, verify only user's tasks displayed with status/dates, filter by status works

### Implementation for User Story 2

- [ ] T025 [P] [US2] Implement TaskService.get_user_tasks method in backend/src/services/task_service.py (query tasks WHERE user_id, apply status filter, order by created_at DESC, return TaskListResponse)
- [ ] T026 [P] [US2] Implement TaskService.get_task_by_id method in backend/src/services/task_service.py (query task WHERE id AND user_id, return TaskResponse or 404)
- [ ] T027 [US2] Implement GET /api/tasks endpoint in backend/src/api/tasks.py (extract user_id, parse status query param, call TaskService.get_user_tasks, return 200 with TaskListResponse)
- [ ] T028 [US2] Implement GET /api/tasks/{id} endpoint in backend/src/api/tasks.py (extract user_id, call TaskService.get_task_by_id, return 200 or 403/404)
- [ ] T029 [P] [US2] Create TaskItem component in frontend/src/components/TaskItem.tsx (display title, description, status, created_at, action buttons)
- [ ] T030 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx (render array of TaskItem, handle empty state, status filter dropdown)
- [ ] T031 [US2] Create task list page in frontend/src/app/page.tsx (fetch tasks from API, render TaskList, implement status filtering)
- [ ] T032 [US2] Add loading and error states to task list page (skeleton loader, error message display, retry button)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task (Priority: P3)

**Goal**: Allow authenticated users to update title and/or description of their tasks

**Independent Test**: Login, select existing task, modify title or description, verify changes persist

### Implementation for User Story 3

- [ ] T033 [US3] Implement TaskService.update_task method in backend/src/services/task_service.py (verify ownership, update fields, update updated_at, return TaskResponse or 403/404)
- [ ] T034 [US3] Implement PUT /api/tasks/{id} endpoint in backend/src/api/tasks.py (extract user_id, validate TaskUpdate, call TaskService.update_task, return 200 or 403/404)
- [ ] T035 [P] [US3] Create task edit page in frontend/src/app/tasks/[id]/page.tsx (fetch task by ID, render TaskForm pre-filled, handle save)
- [ ] T036 [US3] Modify TaskForm component to support edit mode (accept initial values, distinguish create vs update, show appropriate button text)
- [ ] T037 [US3] Add update API call to frontend/src/lib/api.ts (PUT /api/tasks/{id} with TaskUpdateRequest)
- [ ] T038 [US3] Add error handling for update operation (403 forbidden, 404 not found, validation errors, success message)

**Checkpoint**: All user stories 1, 2, AND 3 should now be independently functional

---

## Phase 6: User Story 4 - Delete Task (Priority: P4)

**Goal**: Allow authenticated users to permanently delete their tasks

**Independent Test**: Login, delete one of user's tasks, verify it no longer appears in task list

### Implementation for User Story 4

- [ ] T039 [US4] Implement TaskService.delete_task method in backend/src/services/task_service.py (verify ownership, delete from DB, return success or 403/404)
- [ ] T040 [US4] Implement DELETE /api/tasks/{id} endpoint in backend/src/api/tasks.py (extract user_id, call TaskService.delete_task, return 204 or 403/404)
- [ ] T041 [US4] Add delete API call to frontend/src/lib/api.ts (DELETE /api/tasks/{id})
- [ ] T042 [US4] Add delete button to TaskItem component (confirmation dialog, call delete API, remove from UI on success)
- [ ] T043 [US4] Add error handling for delete operation (403 forbidden, 404 not found, show error message, optimistic UI update)

**Checkpoint**: All user stories 1-4 should now be independently functional

---

## Phase 7: User Story 5 - Toggle Task Completion (Priority: P5)

**Goal**: Allow authenticated users to toggle completion status without updating other fields

**Independent Test**: Login, toggle task completion status, verify status change persists and displays correctly

### Implementation for User Story 5

- [ ] T044 [US5] Implement TaskService.toggle_completion method in backend/src/services/task_service.py (verify ownership, toggle is_complete field, update updated_at, return TaskResponse or 403/404)
- [ ] T045 [US5] Implement PATCH /api/tasks/{id}/toggle endpoint in backend/src/api/tasks.py (extract user_id, call TaskService.toggle_completion, return 200 or 403/404)
- [ ] T046 [US5] Add toggle completion API call to frontend/src/lib/api.ts (PATCH /api/tasks/{id}/toggle)
- [ ] T047 [US5] Add checkbox to TaskItem component (bind to is_complete, call toggle API on change, optimistic UI update)
- [ ] T048 [US5] Add visual styling for completed tasks in TaskItem (strikethrough title, muted colors, completed badge)
- [ ] T049 [US5] Add error handling for toggle operation (403 forbidden, 404 not found, revert UI on failure)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 [P] Add API error handling middleware in backend/src/middleware/error_handler.py (catch exceptions, return consistent error format)
- [ ] T051 [P] Add request logging in backend/src/middleware/logging.py (log all requests with user_id, duration, status code)
- [ ] T052 [P] Add API health check endpoint GET /health in backend/src/main.py (return 200 with status)
- [ ] T053 [P] Add loading spinners to all async operations in frontend (create, update, delete, toggle)
- [ ] T054 [P] Add toast notifications for success/error messages in frontend (create, update, delete, toggle feedback)
- [ ] T055 [P] Implement responsive mobile layout for TaskList and TaskForm (Tailwind breakpoints, mobile-first)
- [ ] T056 [P] Add input sanitization to prevent XSS in TaskForm (trim whitespace, escape HTML in title/description)
- [ ] T057 [P] Add session expiry handling in frontend (detect 401, redirect to login, preserve return URL)
- [ ] T058 Create backend README.md with setup instructions, API documentation, environment variables
- [ ] T059 Create frontend README.md with setup instructions, component overview, environment variables
- [ ] T060 Create .gitignore files for backend (.env, __pycache__, venv) and frontend (node_modules, .next, .env.local)

---

## Phase 9: Reusable Intelligence (BONUS)

**Purpose**: Create reusable agent for task operations as per constitution principle IV

- [ ] T061 Create agent documentation in .specify/agents/task-operations.md (purpose, capabilities, usage examples)
- [ ] T062 Document agent workflows for common patterns (create-task flow, list-filter flow, bulk-update flow)
- [ ] T063 Create skill for task CRUD operations (reusable patterns, error handling, validation logic)
- [ ] T064 Add agent usage examples to project documentation (how to invoke, parameters, expected outputs)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete
- **Reusable Intelligence (Phase 9)**: Can be done anytime after Phase 2, parallel with user stories

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories (independent)

**Key Insight**: All 5 user stories are completely independent after Foundational phase. They can be implemented in parallel by different developers.

### Within Each User Story

- Backend service methods before API endpoints (service → API)
- Backend API before frontend implementation (API → UI)
- Components before pages (components → pages)
- Core functionality before error handling (functionality → errors)

### Parallel Opportunities

- **Setup Phase**: All tasks marked [P] can run in parallel (T003, T004, T005, T006)
- **Foundational Phase**: Many tasks marked [P] can run in parallel (T009-T012, T016-T018)
- **Within User Stories**: Tasks marked [P] within each story can run in parallel
- **Across User Stories**: Once Foundational completes, ALL user stories can be worked on in parallel

---

## Parallel Example: User Story 1

```bash
# Launch models and components together:
Task T019: "Implement TaskService.create_task method in backend/src/services/task_service.py"
Task T021: "Create TaskForm component in frontend/src/components/TaskForm.tsx"

# Then API endpoint and page (after T019 completes):
Task T020: "Implement POST /api/tasks endpoint" (needs T019 done)
Task T022: "Create task creation page" (needs T021 done)

# Then validation and error handling in parallel:
Task T023: "Add form validation"
Task T024: "Add error handling"
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T018) - **CRITICAL BLOCKER**
3. Complete Phase 3: User Story 1 - Create Task (T019-T024)
4. Complete Phase 4: User Story 2 - View Task List (T025-T032)
5. **STOP and VALIDATE**: Test create + view independently
6. Deploy/demo if ready (MVP = Create + View tasks)

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (can create tasks!)
3. Add User Story 2 → Test independently → Deploy/Demo (MVP: create + view!)
4. Add User Story 3 → Test independently → Deploy/Demo (can edit tasks)
5. Add User Story 4 → Test independently → Deploy/Demo (can delete tasks)
6. Add User Story 5 → Test independently → Deploy/Demo (full CRUD!)
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Create Task)
   - Developer B: User Story 2 (View Task List)
   - Developer C: User Story 3 (Update Task)
   - Developer D: User Story 4 (Delete Task)
   - Developer E: User Story 5 (Toggle Completion)
3. Stories complete and integrate independently
4. No merge conflicts (different files per story)

---

## Task Summary

**Total Tasks**: 64 tasks

**Tasks by Phase**:
- Phase 1 (Setup): 6 tasks
- Phase 2 (Foundational): 12 tasks (CRITICAL - blocks all stories)
- Phase 3 (US1 - Create): 6 tasks 🎯 MVP
- Phase 4 (US2 - View): 8 tasks 🎯 MVP
- Phase 5 (US3 - Update): 6 tasks
- Phase 6 (US4 - Delete): 5 tasks
- Phase 7 (US5 - Toggle): 6 tasks
- Phase 8 (Polish): 11 tasks
- Phase 9 (Bonus): 4 tasks

**Parallel Opportunities**: 21 tasks marked [P] can run in parallel with other tasks

**Independent Test Criteria**:
- US1: Create task, verify in database with user_id
- US2: View list, verify only user's tasks shown, filtering works
- US3: Update task, verify changes persist
- US4: Delete task, verify removed from list
- US5: Toggle completion, verify status change persists

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) = 32 tasks
- Delivers: Create and view tasks with authentication
- Independent value: Users can start tracking todos

**Full Feature Scope**: All 64 tasks
- Delivers: Complete CRUD + completion toggle + polish + bonus agent

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- No tests included (not requested in specification)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All file paths are explicit and relative to repository root
- Tasks follow strict checkbox format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
