/**
 * API client utility for Task CRUD Operations and Authentication.
 *
 * This module provides a fetch wrapper with JWT header injection
 * and standardized error handling.
 */

import {
  Task,
  TaskCreateRequest,
  TaskUpdateRequest,
  TaskListResponse,
  TaskStatusFilter,
  ApiError,
  LoginResponse,
  RegisterResponse,
} from "./types";

// API base URL from environment variable
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Get JWT token from storage.
 */
function getAuthToken(): string | null {
  if (typeof window !== "undefined") {
    return localStorage.getItem("auth_token");
  }
  return null;
}

/**
 * Set JWT token in storage.
 */
function setAuthToken(token: string): void {
  if (typeof window !== "undefined") {
    localStorage.setItem("auth_token", token);
  }
}

/**
 * Remove JWT token from storage.
 */
function removeAuthToken(): void {
  if (typeof window !== "undefined") {
    localStorage.removeItem("auth_token");
  }
}

/**
 * Custom error class for API errors.
 */
export class ApiClientError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(detail);
    this.name = "ApiClientError";
  }
}

/**
 * Generic fetch wrapper with JWT authentication.
 *
 * @param endpoint - API endpoint path (relative to base URL)
 * @param options - Fetch options
 * @returns Response data
 * @throws ApiClientError on HTTP errors
 */
async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  // Add Authorization header if token exists
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;

  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    // Handle non-2xx responses
    if (!response.ok) {
      const errorData: ApiError = await response.json().catch(() => ({
        detail: "An unexpected error occurred",
      }));

      throw new ApiClientError(response.status, errorData.detail);
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return null as T;
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ApiClientError) {
      throw error;
    }

    // Network or other errors
    throw new ApiClientError(0, "Network error or server unreachable");
  }
}

/**
 * Register a new user.
 *
 * @param email - User's email
 * @param password - User's password
 * @param fullName - User's full name (optional)
 * @returns Login response with token
 */
export async function register(
  email: string,
  password: string,
  fullName?: string
): Promise<RegisterResponse> {
  const userData = fullName ? { email, password, full_name: fullName } : { email, password };

  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });

  if (!response.ok) {
    let errorDetail = "Registration failed";
    try {
      const errorData: ApiError = await response.json();
      errorDetail = errorData.detail || errorDetail;
    } catch (e) {
      // If JSON parsing fails, use status text
      errorDetail = response.statusText || errorDetail;
    }

    throw new ApiClientError(response.status, errorDetail);
  }

  const data: RegisterResponse = await response.json();
  // Store the token automatically after successful registration
  setAuthToken(data.access_token);
  return data;
}

/**
 * Login user.
 *
 * @param email - User's email
 * @param password - User's password
 * @returns Login response with token
 */
export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const errorData: ApiError = await response.json().catch(() => ({
      detail: "Login failed",
    }));
    throw new ApiClientError(response.status, errorData.detail);
  }

  const data: LoginResponse = await response.json();
  // Store the token automatically after successful login
  setAuthToken(data.access_token);
  return data;
}

/**
 * Logout user.
 */
export async function logout(): Promise<void> {
  try {
    await apiClient<void>("/api/auth/logout", {
      method: "POST",
    });
  } finally {
    // Always remove the token regardless of API call success
    removeAuthToken();
  }
}

/**
 * Get current user info.
 */
export async function getCurrentUser(): Promise<any> {
  return apiClient<any>("/api/auth/me");
}

/**
 * Get list of tasks for the authenticated user.
 *
 * @param statusFilter - Optional filter by completion status
 * @returns Task list response
 */
export async function getTasks(
  statusFilter?: TaskStatusFilter
): Promise<TaskListResponse> {
  const params = new URLSearchParams();
  if (statusFilter && statusFilter !== "all") {
    params.append("status", statusFilter);
  }

  const query = params.toString();
  const endpoint = `/api/tasks${query ? `?${query}` : ""}`;

  return apiClient<TaskListResponse>(endpoint);
}

/**
 * Get a single task by ID.
 *
 * @param taskId - Task ID
 * @returns Task data
 */
export async function getTask(taskId: number): Promise<Task> {
  return apiClient<Task>(`/api/tasks/${taskId}`);
}

/**
 * Create a new task.
 *
 * @param data - Task creation data
 * @returns Created task
 */
export async function createTask(data: TaskCreateRequest): Promise<Task> {
  return apiClient<Task>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing task.
 *
 * @param taskId - Task ID
 * @param data - Task update data
 * @returns Updated task
 */
export async function updateTask(
  taskId: number,
  data: TaskUpdateRequest
): Promise<Task> {
  return apiClient<Task>(`/api/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task.
 *
 * @param taskId - Task ID
 */
export async function deleteTask(taskId: number): Promise<void> {
  return apiClient<void>(`/api/tasks/${taskId}`, {
    method: "DELETE",
  });
}

/**
 * Toggle task completion status.
 *
 * @param taskId - Task ID
 * @returns Updated task
 */
export async function toggleTaskCompletion(taskId: number): Promise<Task> {
  return apiClient<Task>(`/api/tasks/${taskId}/toggle`, {
    method: "PATCH",
  });
}
