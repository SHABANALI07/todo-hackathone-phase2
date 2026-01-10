'use client';

import { useState, useEffect } from 'react';
import { Task, TaskStatusFilter } from '@/lib/types';
import { getTasks } from '@/lib/api';
import TaskList from '@/components/TaskList';
import { ApiClientError } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [statusFilter, setStatusFilter] = useState<TaskStatusFilter>('all');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Fetch tasks on mount and when filter changes
  useEffect(() => {
    loadTasks();
  }, [statusFilter]);

  const loadTasks = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await getTasks(statusFilter);
      setTasks(response.tasks);
    } catch (err: any) {
      if (err instanceof ApiClientError) {
        if (err.status === 401) {
          // Redirect to login if unauthorized
          router.push('/login');
          return;
        } else {
          setError(err.detail);
        }
      } else {
        setError('Failed to load tasks');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Handle task update (from toggle completion)
  const handleTaskUpdate = (updatedTask: Task) => {
    setTasks((prev) =>
      prev.map((task) => (task.id === updatedTask.id ? updatedTask : task))
    );
  };

  // Handle task deletion
  const handleTaskDelete = (taskId: number) => {
    setTasks((prev) => prev.filter((task) => task.id !== taskId));
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">My Tasks</h1>
        <a
          href="/tasks/new"
          className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors"
        >
          + New Task
        </a>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="text-center py-12">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
          <p className="text-red-800">{error}</p>
          <button
            onClick={loadTasks}
            className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
          >
            Retry
          </button>
        </div>
      )}

      {/* Task List */}
      {!isLoading && !error && (
        <TaskList
          tasks={tasks}
          statusFilter={statusFilter}
          onFilterChange={setStatusFilter}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
        />
      )}
    </div>
  );
}