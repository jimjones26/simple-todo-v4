import { render, fireEvent, screen, waitFor, cleanup } from '@testing-library/svelte';
import TaskAssign from '../components/TaskAssign.svelte';
import { patch } from '../utils/api.js';
import { describe, it, expect, vi, afterEach } from 'vitest';

vi.mock('../utils/api.js');

describe('TaskAssign submission', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('submits the form with valid data', async () => {
    patch.mockResolvedValueOnce({ message: 'Task assigned successfully' });

    const task = { id: 1, title: 'Test Task' };
    const users = [{ id: 1, username: 'User 1' }, { id: 2, username: 'User 2' }];

    render(TaskAssign, { props: { task, users } });

    const selectElement = screen.getByLabelText('Select user:');
    const assignButton = screen.getByText('Assign');

    // Select a user
    await fireEvent.change(selectElement, { target: { value: '1' } });

    // Click the assign button
    await fireEvent.click(assignButton);

    // Check if the patch function was called with the correct arguments
    expect(patch).toHaveBeenCalledTimes(1);
    expect(patch).toHaveBeenCalledWith(`/tasks/${task.id}/assign`, { user_id: 1 });

    // Check if the success message is displayed
    await waitFor(() => {
      expect(screen.getByText('User assigned successfully!')).toBeInTheDocument();
    });
  });

  it('shows an error message on submission failure', async () => {
    patch.mockRejectedValueOnce(new Error('Failed to assign user'));

    const task = { id: 1, title: 'Test Task' };
    const users = [{ id: 1, username: 'User 1' }, { id: 2, username: 'User 2' }];

    render(TaskAssign, { props: { task, users } });

    const selectElement = screen.getByLabelText('Select user:');
    const assignButton = screen.getByText('Assign');

    // Select a user
    await fireEvent.change(selectElement, { target: { value: 1 } });

    // Click the assign button
    await fireEvent.click(assignButton);

    // Check if the error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to assign user')).toBeInTheDocument();
    });
  });
});
