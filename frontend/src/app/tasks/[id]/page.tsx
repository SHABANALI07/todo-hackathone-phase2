"use client";

/**
 * Edit Task Page
 *
 * Page for editing an existing task.
 */

import { useRouter, useParams } from "next/navigation";
import { useState, useEffect } from "react";
import { Task, TaskUpdateRequest } from "@/lib/types";
import { getTask, updateTask, ApiClientError } from "@/lib/api";
import TaskForm from "@/components/TaskForm";

export default function EditTaskPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = parseInt(params.id as string);

  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Load task on mount
  useEffect(() => {
    loadTask();
  }, [taskId]);

  const loadTask = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const fetchedTask = await getTask(taskId);
      setTask(fetchedTask);
    } catch (err: any) {
      if (err instanceof ApiClientError && err.status === 401) {
        // Redirect to login if unauthorized
        router.push('/login');
        return;
      }
      setError(err.detail || err.message || "Failed to load task");
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (data: TaskUpdateRequest) => {
    setError(null);
    setSuccessMessage(null);

    try {
      await updateTask(taskId, data);
      setSuccessMessage("Task updated successfully!");

      // Redirect to home page after 1 second
      setTimeout(() => {
        router.push("/");
      }, 1000);
    } catch (err: any) {
      if (err instanceof ApiClientError && err.status === 401) {
        // Redirect to login if unauthorized
        router.push('/login');
        return;
      }
      setError(err.detail || err.message || "Failed to update task");
      throw err; // Re-throw to let form handle it
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Edit Task</h1>
        <p className="mt-2 text-gray-600">Update the details for your task.</p>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading task...</p>
        </div>
      )}

      {/* Success Message */}
      {successMessage && (
        <div className="mb-6 bg-green-50 border border-green-200 rounded-md p-4">
          <p className="text-green-800">{successMessage}</p>
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800">{error}</p>
          {!task && (
            <button
              onClick={loadTask}
              className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
            >
              Retry
            </button>
          )}
        </div>
      )}

      {/* Task Form */}
      {task && !isLoading && (
        <div className="bg-white p-6 rounded-lg shadow-md">
          <TaskForm
            initialTitle={task.title}
            initialDescription={task.description || ""}
            onSubmit={handleSubmit}
            submitLabel="Update Task"
            isEdit={true}
          />
        </div>
      )}

      {/* Back Link */}
      <div className="mt-4">
        <a href="/" className="text-primary-600 hover:text-primary-700 underline">
          ← Back to Task List
        </a>
      </div>
    </div>
  );
}
