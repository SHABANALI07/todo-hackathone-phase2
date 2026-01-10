/**
 * TypeScript type definitions for Task CRUD Operations and Authentication.
 *
 * This module defines the data structures used throughout the frontend
 * for task management with user isolation and authentication.
 */

/**
 * Task entity representing a todo item
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_complete: boolean;
  created_at: string; // ISO 8601 datetime string
  updated_at: string; // ISO 8601 datetime string
  user_id: number;
}

/**
 * User entity representing an authenticated user
 */
export interface User {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string; // ISO 8601 datetime string
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
 * Status filter options for task list
 */
export type TaskStatusFilter = "all" | "complete" | "incomplete";

/**
 * API error response structure
 */
export interface ApiError {
  detail: string;
}

/**
 * Response from login endpoint
 */
export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

/**
 * Response from register endpoint
 */
export interface RegisterResponse {
  access_token: string;
  token_type: string;
  user: User;
}
