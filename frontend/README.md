# Todo App - Frontend

Next.js 14 frontend for Task CRUD Operations with TypeScript and Tailwind CSS.

## Features

- ✅ Complete task management UI
- ✅ Create, view, update, delete tasks
- ✅ Toggle task completion with optimistic UI updates
- ✅ Status filtering (all, complete, incomplete)
- ✅ JWT authentication integration
- ✅ Responsive design (mobile and desktop)
- ✅ Real-time form validation
- ✅ Loading and error states

## Tech Stack

- **Next.js 14+** - React framework with App Router
- **TypeScript 5.x** - Type-safe development
- **Tailwind CSS 3.x** - Utility-first CSS framework
- **React 18+** - UI library

## Setup

### 1. Install Dependencies

```bash
cd frontend

# Install packages
npm install
# or
yarn install
```

### 2. Environment Variables

Create a `.env.local` file (copy from `.env.local.example`):

```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your configuration:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=same-secret-as-backend
BETTER_AUTH_URL=http://localhost:8000/api/auth
```

### 3. Run the Development Server

```bash
npm run dev
# or
yarn dev
```

The application will be available at http://localhost:3000

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/task list page
│   │   ├── globals.css      # Global styles
│   │   └── tasks/
│   │       ├── new/
│   │       │   └── page.tsx # Create task page
│   │       └── [id]/
│   │           └── page.tsx # Edit task page
│   ├── components/
│   │   ├── TaskList.tsx     # Task list with filtering
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   └── TaskItem.tsx     # Individual task display
│   └── lib/
│       ├── api.ts           # API client with JWT headers
│       └── types.ts         # TypeScript type definitions
├── package.json
├── tsconfig.json
├── tailwind.config.js
├── next.config.js
└── README.md
```

## Pages

### Home Page (`/`)

- Displays all user tasks
- Filter by status (all/complete/incomplete)
- Toggle task completion
- Delete tasks with confirmation
- Navigate to edit page
- Link to create new task

### Create Task Page (`/tasks/new`)

- Form to create new task
- Title input (required, 1-200 chars)
- Description textarea (optional, max 1000 chars)
- Real-time validation
- Success/error messages
- Auto-redirect to home on success

### Edit Task Page (`/tasks/[id]`)

- Pre-filled form with existing task data
- Update title and/or description
- Same validation as create
- Success/error messages
- Auto-redirect to home on success

## Components

### TaskList

Displays a filterable list of tasks with status dropdown.

**Props:**
- `tasks`: Array of Task objects
- `statusFilter`: Current filter value
- `onFilterChange`: Callback for filter changes
- `onTaskUpdate`: Callback when task is updated
- `onTaskDelete`: Callback when task is deleted

### TaskForm

Reusable form for creating and editing tasks.

**Props:**
- `initialTitle`: Pre-filled title (for edit mode)
- `initialDescription`: Pre-filled description (for edit mode)
- `onSubmit`: Callback with form data
- `submitLabel`: Button text (default: "Create Task")
- `isEdit`: Boolean to indicate edit mode

### TaskItem

Displays a single task with actions.

**Props:**
- `task`: Task object
- `onUpdate`: Callback when task is updated
- `onDelete`: Callback when task is deleted

**Features:**
- Checkbox for toggle completion
- Strikethrough for completed tasks
- Edit button (navigates to edit page)
- Delete button with confirmation

## API Integration

The `lib/api.ts` module provides functions for all API operations:

```typescript
// Get tasks with optional filtering
const response = await getTasks('incomplete');

// Get single task
const task = await getTask(taskId);

// Create task
const newTask = await createTask({ title: 'Todo', description: 'Description' });

// Update task
const updated = await updateTask(taskId, { title: 'New title' });

// Delete task
await deleteTask(taskId);

// Toggle completion
const toggled = await toggleTaskCompletion(taskId);
```

All functions:
- Automatically include JWT token from localStorage
- Handle errors with ApiClientError
- Return typed responses

## Authentication

**Current Implementation:**

The API client expects JWT tokens to be stored in `localStorage` under the key `auth_token`.

**To integrate with Better Auth:**

1. Update `getAuthToken()` in `lib/api.ts` to retrieve tokens from Better Auth
2. Implement login/logout pages
3. Add protected route middleware
4. Handle 401 responses with redirect to login

## Styling

### Tailwind CSS

The app uses Tailwind CSS for styling with a custom theme defined in `tailwind.config.js`.

**Primary colors:**
- 50-900 scale for primary brand color (blue)
- Responsive breakpoints for mobile/desktop

**Common utilities:**
- `container mx-auto` - Centered container
- `px-4 py-2` - Padding
- `rounded-md` - Rounded corners
- `shadow-sm` - Subtle shadow

### Global Styles

Global CSS is defined in `app/globals.css` with Tailwind directives.

## Development

### Build for Production

```bash
npm run build
npm start
```

### Linting

```bash
npm run lint
```

### Type Checking

TypeScript will automatically check types during development. For explicit checking:

```bash
npx tsc --noEmit
```

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import project in Vercel
3. Set environment variables
4. Deploy

### Other Platforms

1. Build the app: `npm run build`
2. Start production server: `npm start`
3. Ensure environment variables are set

## Troubleshooting

### API Connection Error

Ensure:
- Backend is running on the correct port
- `NEXT_PUBLIC_API_URL` is correct
- CORS is configured on backend

### Authentication Errors

Verify:
- JWT token is stored in localStorage
- Token is not expired
- `BETTER_AUTH_SECRET` matches backend

### TypeScript Errors

Run:
```bash
npm run lint
npx tsc --noEmit
```

## Future Enhancements

- [ ] Better Auth integration for login/logout
- [ ] Toast notifications for success/error messages
- [ ] Loading skeletons for better UX
- [ ] Task search functionality
- [ ] Task categories/tags
- [ ] Due dates
- [ ] Dark mode

## License

MIT License
