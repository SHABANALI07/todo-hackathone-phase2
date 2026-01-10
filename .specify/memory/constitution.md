<!--
Sync Impact Report:
- Version: NEW → 1.0.0 (Initial constitution for Todo Hackathon Phase II project)
- Added principles: Spec-Driven Development, Security & User Isolation, Clean Architecture, Reusable Intelligence
- Added sections: Technology Stack, Constraints, Governance
- Templates status:
  ✅ plan-template.md - Constitution Check section aligns with new principles
  ✅ spec-template.md - Requirements structure supports security and user story approach
  ✅ tasks-template.md - Task organization supports modular implementation
- Follow-up: None - all placeholders filled
-->

# Todo Hackathon Phase II Constitution

## Project Overview

Full-stack multi-user web todo application with authentication and persistent storage, built entirely through Spec-Driven Development principles using Claude Code agents.

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

All code MUST be generated from specifications via Claude Code agents. Manual code changes are prohibited.

**Requirements:**
- Every feature begins with a specification document
- Implementation follows the SDD workflow: spec → plan → tasks → implementation
- Agents and skills handle all code generation and modifications
- Documentation precedes implementation in all cases

**Rationale:** Ensures consistency, traceability, and leverages AI-assisted development to maximize development velocity while maintaining quality standards.

### II. Security & User Isolation (NON-NEGOTIABLE)

User data MUST be completely isolated with mandatory authentication for all operations.

**Requirements:**
- JWT-based authentication via Better Auth for all API requests
- Every database query MUST filter by authenticated user_id
- No user can access, modify, or view another user's tasks
- Authentication token validation required at API boundary
- Shared secret (BETTER_AUTH_SECRET) used for token verification

**Rationale:** Multi-user application requires strict data isolation to protect user privacy and prevent unauthorized access.

### III. Clean Architecture

Monorepo structure with clear separation between frontend presentation and backend business logic.

**Requirements:**
- Frontend: Next.js App Router with TypeScript and Tailwind CSS
- Backend: FastAPI with SQLModel for database operations
- RESTful API contract under /api/tasks endpoints
- Frontend communicates only through defined API contracts
- Database operations isolated to backend services

**Rationale:** Separation of concerns enables independent development, testing, and scaling of frontend and backend systems.

### IV. Reusable Intelligence (BONUS OBJECTIVE)

Implement agents and skills for common task operations to demonstrate advanced automation capabilities.

**Requirements:**
- Create reusable Claude Code agents for complex workflows
- Develop skills for repetitive task operations
- Document agent and skill implementations
- Ensure agents follow project constitution and standards

**Rationale:** Demonstrates advanced AI-assisted development patterns and provides reusable automation for future development work.

## Technology Stack

### Frontend
- **Framework**: Next.js (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React hooks and server components
- **API Client**: Fetch API with JWT token headers

### Backend
- **Framework**: FastAPI
- **Language**: Python
- **ORM**: SQLModel
- **Database**: Neon PostgreSQL
- **Authentication**: Better Auth with JWT tokens

### Database Schema
- **tasks table**: Core entity with user_id foreign key
- **users table**: Authentication and profile data
- **All tables**: Include user_id for multi-tenancy enforcement

## Constraints

### Development Process
- **No Manual Coding**: All implementation through Claude Code specs and agents
- **Spec-First**: No code without specification
- **Auth-First**: All API endpoints require valid JWT authentication
- **User-Scoped**: All data operations filtered by authenticated user_id

### Security
- **Shared Secret**: BETTER_AUTH_SECRET environment variable for token signing
- **Token Validation**: JWT verification on every API request
- **Data Isolation**: Automatic user_id filtering in all database queries
- **No Direct Access**: Frontend cannot directly access database

### Quality
- **Type Safety**: TypeScript on frontend, type hints on backend
- **Responsive Design**: Mobile-first Tailwind implementation
- **Error Handling**: Graceful degradation for auth and API failures
- **Data Persistence**: All state persisted to Neon database

## Success Criteria

The project is considered complete when ALL of the following are met:

1. **Authentication**:
   - Users can sign up with email/password
   - Users can log in and receive JWT token
   - Invalid credentials are rejected gracefully

2. **Task Operations**:
   - Logged-in users can create tasks
   - Users can view only their own tasks
   - Users can update their own tasks
   - Users can delete their own tasks
   - All operations require valid JWT token

3. **Data Persistence**:
   - All tasks stored in Neon PostgreSQL
   - Data survives application restarts
   - User data is completely isolated

4. **User Experience**:
   - Responsive UI works on mobile and desktop
   - Clear feedback for all operations
   - Loading and error states handled

5. **Advanced Implementation** (BONUS):
   - Agents implemented for complex workflows
   - Skills created for repetitive operations
   - Reusable intelligence documented

6. **Spec-Driven Compliance**:
   - All features implemented from specifications
   - Complete audit trail from spec to code
   - No manual code modifications

## Governance

### Amendment Process
- Constitution updates require documentation in Prompt History Records (PHRs)
- Version number MUST be incremented following semantic versioning
- Changes propagated to dependent templates and documentation
- All amendments recorded with rationale and impact analysis

### Compliance Verification
- All specifications MUST reference constitution principles
- Implementation plans MUST include Constitution Check section
- Tasks MUST align with architectural constraints
- Code reviews verify adherence to security and isolation requirements

### Version Management
- MAJOR: Backward incompatible principle changes (e.g., removing authentication requirement)
- MINOR: New principles added or expanded guidance (e.g., adding observability requirements)
- PATCH: Clarifications, wording improvements, non-semantic refinements

### PHR Creation
- Record every user interaction in Prompt History Records
- Route to appropriate directory: constitution/, feature-name/, or general/
- Include full prompt text and response summary
- Validate no unresolved placeholders

### Architectural Decision Records
- Suggest ADR creation for significant decisions during planning
- Never auto-create ADRs without user consent
- Follow three-part test: Impact + Alternatives + Scope

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
