"use client";

/**
 * Task Item Component
 *
 * Displays a single task with checkbox, details, and action buttons.
 */

import { Task } from "@/lib/types";
import { toggleTaskCompletion, deleteTask, ApiClientError } from "@/lib/api";
import { useState } from "react";
import { useRouter } from 'next/navigation';

interface TaskItemProps {
  task: Task;
  onUpdate: (updatedTask: Task) => void;
  onDelete: (taskId: number) => void;
}

export default function TaskItem({ task, onUpdate, onDelete }: TaskItemProps) {
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const router = useRouter();

  // Handle toggle completion
  const handleToggle = async () => {
    setIsToggling(true);
    try {
      const updatedTask = await toggleTaskCompletion(task.id);
      onUpdate(updatedTask);
    } catch (error: any) {
      if (error instanceof ApiClientError && error.status === 401) {
        // Redirect to login if unauthorized
        router.push('/login');
        return;
      }
      alert(`Failed to toggle task: ${error.detail || error.message}`);
      setIsToggling(false);
    }
  };

  // Handle delete with confirmation
  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this task?")) {
      return;
    }

    setIsDeleting(true);
    try {
      await deleteTask(task.id);
      onDelete(task.id);
    } catch (error: any) {
      if (error instanceof ApiClientError && error.status === 401) {
        // Redirect to login if unauthorized
        router.push('/login');
        return;
      }
      alert(`Failed to delete task: ${error.detail || error.message}`);
      setIsDeleting(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div
      className={`p-4 border rounded-lg shadow-sm transition-all ${
        task.is_complete ? "bg-gray-50 border-gray-300" : "bg-white border-gray-200"
      } ${isDeleting ? "opacity-50" : ""}`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={task.is_complete}
          onChange={handleToggle}
          disabled={isToggling || isDeleting}
          className="mt-1 h-5 w-5 text-primary-600 rounded focus:ring-2 focus:ring-primary-500 cursor-pointer"
        />

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {/* Title */}
          <h3
            className={`text-lg font-medium ${
              task.is_complete ? "line-through text-gray-500" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>

          {/* Description */}
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.is_complete ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}

          {/* Metadata */}
          <div className="mt-2 flex items-center gap-4 text-xs text-gray-500">
            <span>Created: {formatDate(task.created_at)}</span>
            {task.is_complete && (
              <span className="px-2 py-1 bg-green-100 text-green-800 rounded-full">
                Completed
              </span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2">
          {/* Edit Button */}
          <a
            href={`/tasks/${task.id}`}
            className="px-3 py-1 text-sm text-primary-600 border border-primary-600 rounded hover:bg-primary-50 transition-colors"
          >
            Edit
          </a>

          {/* Delete Button */}
          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="px-3 py-1 text-sm text-red-600 border border-red-600 rounded hover:bg-red-50 transition-colors disabled:opacity-50"
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>
    </div>
  );
}
