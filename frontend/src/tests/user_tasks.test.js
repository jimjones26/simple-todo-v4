// @ts-nocheck
import { render, cleanup } from '@testing-library/svelte';
import UserTasks from '../components/UserTasks.svelte';
import { vi, describe, it, expect, afterEach } from 'vitest';
import { auth } from '../stores/authStore'; // Import the auth store
import * as api from '../utils/api'; // Import the api module for mocking

describe('UserTasks.svelte', () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks(); // Restore all mocks to their original state
  });

  it('should render the component', () => {
    const { getByText } = render(UserTasks);
    expect(getByText('My Tasks')).toBeInTheDocument();
  });

  it('should render a loading message initially when user is logged in', () => {
    // Set the auth store to simulate a logged-in user
    auth.set({ user: { id: 1 } });
    const { getByText } = render(UserTasks);
    expect(getByText('Loading tasks...')).toBeInTheDocument();
  });

  it('should render an error message when user is not logged in', () => {
    // Set the auth store to simulate no user
    auth.set({ user: null });
    const { getByText } = render(UserTasks);
    expect(getByText('Error: User not logged in.')).toBeInTheDocument();
  });

  it('should render a list of tasks when user is logged in and tasks are fetched', async () => {
    // Set the auth store to simulate a logged-in user
    auth.set({ user: { id: 1 } });
    // Mock the API call to return tasks
    vi.spyOn(api, 'get').mockResolvedValue([
      { id: 1, title: 'Task 1', description: 'Desc 1', status: 'Open' }
    ]);
    const { findByRole } = render(UserTasks);
    const taskList = await findByRole('list'); // <ul> has role="list" by default
    expect(taskList).toBeInTheDocument();
  });

  it('should render a message if there are no tasks', async () => {
    // Set the auth store to simulate a logged-in user
    auth.set({ user: { id: 1 } });
    // Mock the API call to return an empty task list
    vi.spyOn(api, 'get').mockResolvedValue([]);
    const { findByText } = render(UserTasks);
    expect(await findByText('No tasks assigned.')).toBeInTheDocument();
  });
});