// @ts-nocheck
import { render, cleanup, waitFor } from '@testing-library/svelte';
import UserTasks from '../components/UserTasks.svelte';
import { get } from '../utils/api';
import { auth } from '../stores/authStore';
import { vi, describe, it, expect, afterEach, beforeEach } from 'vitest';

vi.mock('../utils/api');

describe('UserTasks.svelte - Fetching', () => {
  beforeEach(() => {
    // Set a mock user in the auth store
    auth.set({ isAuthenticated: true, user: { id: 123 }, isLoading: false });
  });

  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
    auth.set({ isAuthenticated: false, user: null, isLoading: false });
  });

  it('fetches and displays tasks correctly', async () => {
    // Mock the API response
    const mockTasks = [
      { id: 1, title: 'Task 1', description: 'Description 1', status: 'not started', deadline: null, team_id: 1, assignee_id: 123 },
      { id: 2, title: 'Task 2', description: 'Description 2', status: 'in progress', deadline: '2024-05-30T12:00:00Z', team_id: 1, assignee_id: 123 },
    ];
    get.mockResolvedValue(mockTasks);

    const { getByText, queryByText, findByText } = render(UserTasks);

    // Initially, loading message should be displayed
    expect(getByText('Loading tasks...')).toBeInTheDocument();

    // Wait for the tasks to be fetched and displayed
    const task1Title = await findByText('Task 1');
    const task2Title = await findByText('Task 2');
    expect(task1Title).toBeInTheDocument();
    expect(task2Title).toBeInTheDocument();

    // Check for task details
    expect(getByText('Description 1')).toBeInTheDocument();
    expect(getByText('Status: not started')).toBeInTheDocument();
    expect(getByText('Status: in progress')).toBeInTheDocument();
    expect(getByText('Deadline: 2024-05-30T12:00:00Z')).toBeInTheDocument();

    // Loading message should be gone
    expect(queryByText('Loading tasks...')).not.toBeInTheDocument();
  });

  it('handles API errors gracefully', async () => {
    // Mock an API error
    get.mockRejectedValue(new Error('Failed to fetch tasks.'));

    const { getByText, queryByText, findByText } = render(UserTasks);

    // Initially, loading message should be displayed
    expect(getByText('Loading tasks...')).toBeInTheDocument();

    // Wait for the error message to be displayed
    const errorMessage = await findByText('Error: Failed to fetch tasks.');
    expect(errorMessage).toBeInTheDocument();

    // Loading message should be gone
    expect(queryByText('Loading tasks...')).not.toBeInTheDocument();
    // No tasks message should not be present
    expect(queryByText('No tasks assigned.')).not.toBeInTheDocument();
  });

  it('displays "No tasks assigned." when the API returns an empty array', async () => {
    get.mockResolvedValue([]); // Mock an empty task list

    const { getByText, queryByText, findByText } = render(UserTasks);

    expect(getByText('Loading tasks...')).toBeInTheDocument();

    const noTasksMessage = await findByText('No tasks assigned.');
    expect(noTasksMessage).toBeInTheDocument();
    expect(queryByText('Loading tasks...')).not.toBeInTheDocument();
  });

  it('handles user not logged in', async () => {
    // Simulate user not being logged in
    auth.set({ isAuthenticated: false, user: null, isLoading: false });

    const { getByText, queryByText } = render(UserTasks);

    // Check for error message
    expect(getByText('Error: User not logged in.')).toBeInTheDocument();

    // Loading message and no tasks message should not be present
    expect(queryByText('Loading tasks...')).not.toBeInTheDocument();
    expect(queryByText('No tasks assigned.')).not.toBeInTheDocument();
  });
});
