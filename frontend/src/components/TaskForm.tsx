"use client";

/**
 * Task Form Component
 *
 * Reusable form for creating and editing tasks.
 * Supports both create mode (empty form) and edit mode (pre-filled).
 */

import { useState, FormEvent } from "react";
import { TaskCreateRequest, TaskUpdateRequest } from "@/lib/types";
import { ApiClientError } from "@/lib/api";
import { useRouter } from 'next/navigation';

interface TaskFormProps {
  initialTitle?: string;
  initialDescription?: string;
  onSubmit: (data: TaskCreateRequest | TaskUpdateRequest) => Promise<void>;
  submitLabel?: string;
  isEdit?: boolean;
}

export default function TaskForm({
  initialTitle = "",
  initialDescription = "",
  onSubmit,
  submitLabel = "Create Task",
  isEdit = false,
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [errors, setErrors] = useState<{ title?: string; description?: string }>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const router = useRouter();

  // Validation function
  const validate = (): boolean => {
    const newErrors: { title?: string; description?: string } = {};

    // Title validation
    const trimmedTitle = title.trim();
    if (!trimmedTitle) {
      newErrors.title = "Title is required";
    } else if (trimmedTitle.length > 200) {
      newErrors.title = "Title cannot exceed 200 characters";
    }

    // Description validation
    if (description && description.length > 1000) {
      newErrors.description = "Description cannot exceed 1000 characters";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  // Handle form submission
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    if (!validate()) {
      return;
    }

    setIsSubmitting(true);
    setErrors({});

    try {
      const trimmedTitle = title.trim();
      const trimmedDescription = description.trim() || null;

      await onSubmit({
        title: trimmedTitle,
        description: trimmedDescription,
      });

      // Clear form if not in edit mode
      if (!isEdit) {
        setTitle("");
        setDescription("");
      }
    } catch (error: any) {
      if (error instanceof ApiClientError && error.status === 401) {
        // Redirect to login if unauthorized
        router.push('/login');
        return;
      }
      // Display error from API
      setErrors({ title: error.detail || error.message || "An error occurred" });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Title Input */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          onBlur={validate}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 ${
            errors.title ? "border-red-500" : "border-gray-300"
          }`}
          placeholder="Enter task title"
          maxLength={200}
          disabled={isSubmitting}
        />
        {errors.title && <p className="mt-1 text-sm text-red-600">{errors.title}</p>}
        <p className="mt-1 text-xs text-gray-500">{title.length}/200 characters</p>
      </div>

      {/* Description Textarea */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onBlur={validate}
          rows={4}
          className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 ${
            errors.description ? "border-red-500" : "border-gray-300"
          }`}
          placeholder="Enter task description (optional)"
          maxLength={1000}
          disabled={isSubmitting}
        />
        {errors.description && (
          <p className="mt-1 text-sm text-red-600">{errors.description}</p>
        )}
        <p className="mt-1 text-xs text-gray-500">{description.length}/1000 characters</p>
      </div>

      {/* Submit Button */}
      <div>
        <button
          type="submit"
          disabled={isSubmitting || !title.trim()}
          className={`w-full px-4 py-2 text-white rounded-md transition-colors ${
            isSubmitting || !title.trim()
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-primary-600 hover:bg-primary-700"
          }`}
        >
          {isSubmitting ? "Saving..." : submitLabel}
        </button>
      </div>
    </form>
  );
}
