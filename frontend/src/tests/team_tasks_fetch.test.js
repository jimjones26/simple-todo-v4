// @ts-nocheck
import { render, screen, waitFor, cleanup } from '@testing-library/svelte';
import TeamTasks from '../components/TeamTasks.svelte';
import { get } from '../utils/api';
import { vi, describe, it, expect, afterEach } from 'vitest';

vi.mock('../utils/api');

describe('TeamTasks Component - Task Fetching', () => {
  // Clean up after each test to ensure DOM isolation
  afterEach(() => {
    cleanup();
  });

  it('fetches and displays tasks on mount', async () => {
    // Arrange: Mock the API response
    const mockTeamId = 1;
    const mockTasks = [
      { id: 1, title: 'Task 1', description: 'Description 1', status: 'not started' },
      { id: 2, title: 'Task 2', description: 'Description 2', status: 'in progress' },
    ];
    get.mockResolvedValue(mockTasks);

    // Act: Render the component
    render(TeamTasks, { props: { teamId: mockTeamId } });

    // Assert: Check that the loading message is initially displayed
    expect(screen.getByText('Loading tasks...')).toBeInTheDocument();

    // Assert: Wait for the API call to complete and tasks to be displayed
    await waitFor(() => {
      expect(screen.getByText('Task 1')).toBeInTheDocument();
      expect(screen.getByText('Description 1')).toBeInTheDocument();
      expect(screen.getByText('Task 2')).toBeInTheDocument();
      expect(screen.getByText('Description 2')).toBeInTheDocument();
    });

    // Assert: Verify the API was called with the correct endpoint
    expect(get).toHaveBeenCalledWith(`/teams/${mockTeamId}/tasks`);
  });

  it('displays an error message if fetching tasks fails', async () => {
    // Arrange
    const mockTeamId = 1;
    get.mockRejectedValue(new Error('Failed to fetch tasks'));

    // Act
    render(TeamTasks, { props: { teamId: mockTeamId } });

    // Assert: Check for error message (corrected text without period)
    await waitFor(() => {
      expect(screen.getByText('Error: Failed to fetch tasks')).toBeInTheDocument();
    });
  });

  it('displays a message if there are no tasks', async () => {
    const mockTeamId = 1;
    get.mockResolvedValue([]);

    render(TeamTasks, { props: { teamId: mockTeamId } });

    await waitFor(() => {
      expect(screen.getByText('No tasks for this team.')).toBeInTheDocument();
    });
  });
});