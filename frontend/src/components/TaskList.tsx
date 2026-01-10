"use client";

/**
 * Task List Component
 *
 * Displays a list of tasks with status filtering.
 */

import { Task, TaskStatusFilter } from "@/lib/types";
import TaskItem from "./TaskItem";

interface TaskListProps {
  tasks: Task[];
  statusFilter: TaskStatusFilter;
  onFilterChange: (filter: TaskStatusFilter) => void;
  onTaskUpdate: (updatedTask: Task) => void;
  onTaskDelete: (taskId: number) => void;
}

export default function TaskList({
  tasks,
  statusFilter,
  onFilterChange,
  onTaskUpdate,
  onTaskDelete,
}: TaskListProps) {
  return (
    <div className="space-y-4">
      {/* Filter Dropdown */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Your Tasks</h2>
        <div className="flex items-center gap-2">
          <label htmlFor="status-filter" className="text-sm font-medium text-gray-700">
            Filter:
          </label>
          <select
            id="status-filter"
            value={statusFilter}
            onChange={(e) => onFilterChange(e.target.value as TaskStatusFilter)}
            className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Tasks</option>
            <option value="incomplete">Incomplete</option>
            <option value="complete">Complete</option>
          </select>
        </div>
      </div>

      {/* Task Count */}
      <p className="text-sm text-gray-600">
        Showing {tasks.length} {tasks.length === 1 ? "task" : "tasks"}
      </p>

      {/* Task List */}
      {tasks.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed border-gray-300">
          <p className="text-gray-500 text-lg">No tasks found</p>
          <p className="text-gray-400 text-sm mt-2">
            {statusFilter === "all"
              ? "Create your first task to get started!"
              : `No ${statusFilter} tasks yet.`}
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onUpdate={onTaskUpdate}
              onDelete={onTaskDelete}
            />
          ))}
        </div>
      )}
    </div>
  );
}
