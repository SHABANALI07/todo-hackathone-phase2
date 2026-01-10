"use client";

/**
 * New Task Page
 *
 * Page for creating a new task.
 */

import { useRouter } from "next/navigation";
import { TaskCreateRequest } from "@/lib/types";
import { createTask, ApiClientError } from "@/lib/api";
import TaskForm from "@/components/TaskForm";
import { useState } from "react";

export default function NewTaskPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleSubmit = async (data: TaskCreateRequest) => {
    setError(null);
    setSuccessMessage(null);

    try {
      await createTask(data);
      setSuccessMessage("Task created successfully!");

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
      setError(err.detail || err.message || "Failed to create task");
      throw err; // Re-throw to let form handle it
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Create New Task</h1>
        <p className="mt-2 text-gray-600">Fill in the details for your new task.</p>
      </div>

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
        </div>
      )}

      {/* Task Form */}
      <div className="bg-white p-6 rounded-lg shadow-md">
        <TaskForm onSubmit={handleSubmit} submitLabel="Create Task" />
      </div>

      {/* Back Link */}
      <div className="mt-4">
        <a href="/" className="text-primary-600 hover:text-primary-700 underline">
          ← Back to Task List
        </a>
      </div>
    </div>
  );
}
