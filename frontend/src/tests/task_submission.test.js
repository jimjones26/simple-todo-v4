// @ts-nocheck
import { render, fireEvent, screen, waitFor, cleanup } from '@testing-library/svelte';
import TaskForm from '../components/TaskForm.svelte';
import { post } from '../utils/api.js';
import { describe, it, expect, vi, afterEach } from 'vitest';

vi.mock('../utils/api.js');

describe('TaskForm submission', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('submits the form with valid data', async () => {
    post.mockResolvedValueOnce({ id: 1, title: 'Test Task', description: 'Test Description', team_id: 1 });

    render(TaskForm, { props: { teams: [{ id: 1, name: 'Team 1' }] } });

    const titleInput = screen.getByLabelText('Title:');
    const descriptionInput = screen.getByLabelText('Description:');
    const teamSelect = screen.getByLabelText('Team:');
    const submitButton = screen.getByText('Create Task');

    await fireEvent.input(titleInput, { target: { value: 'Test Task' } });
    await fireEvent.input(descriptionInput, { target: { value: 'Test Description' } });
    await fireEvent.change(teamSelect, { target: { value: '1' } });
    await fireEvent.click(submitButton);

    expect(post).toHaveBeenCalledTimes(1);
    expect(post).toHaveBeenCalledWith('/tasks', {
      title: 'Test Task',
      description: 'Test Description',
      team_id: 1,
    });

    await waitFor(() => {
      expect(screen.getByText('Task created successfully!')).toBeInTheDocument();
    });
  });

  it('shows an error message on submission failure', async () => {
    post.mockRejectedValueOnce(new Error('Failed to create task'));

    render(TaskForm, { props: { teams: [{ id: 1, name: 'Team 1' }] } });

    const titleInput = screen.getByLabelText('Title:');
    const descriptionInput = screen.getByLabelText('Description:');
    const teamSelect = screen.getByLabelText('Team:');
    const submitButton = screen.getByText('Create Task');

    await fireEvent.input(titleInput, { target: { value: 'Test Task' } });
    await fireEvent.input(descriptionInput, { target: { value: 'Test Description' } });
    await fireEvent.change(teamSelect, { target: { value: '1' } });
    await fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText('Failed to create task')).toBeInTheDocument();
    });
  });
});
