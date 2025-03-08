// @ts-nocheck
import { render, fireEvent, waitFor, cleanup } from '@testing-library/svelte';
import { describe, it, afterEach, vi, expect } from 'vitest';
import TaskDeadline from '../components/TaskDeadline.svelte';
import { patch } from '../utils/api.js';

vi.mock('../utils/api.js');

describe('Deadline Form Submission', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  const mockTasks = [
    { id: 1, title: 'Task 1', team_id: 1 },
    { id: 2, title: 'Task 2', team_id: 1 }
  ];

  it('submits selected task and deadline to API', async () => {
    const mockDate = new Date('2024-06-01T12:00');
    patch.mockResolvedValue({ ok: true });

    const { getByLabelText, getByRole } = render(TaskDeadline, {
      props: { tasks: mockTasks }
    });

    // Select a task
    await fireEvent.change(getByLabelText('Task:'), { target: { value: '2' } });

    // Set deadline
    const dateInput = getByLabelText('Deadline:');
    await fireEvent.input(dateInput, { target: { value: '2024-06-01T12:00' } });

    // Submit form
    await fireEvent.click(getByRole('button', { name: 'Set Deadline' }));

    await waitFor(() => {
      expect(patch).toHaveBeenCalledWith(
        '/tasks/2/deadline',
        { deadline: mockDate.toISOString() }
      );
    });
  });

  it('shows error message on API failure', async () => {
    patch.mockRejectedValue(new Error('Server error'));

    const { getByLabelText, getByRole, findByText } = render(TaskDeadline, {
      props: { tasks: mockTasks }
    });

    await fireEvent.change(getByLabelText('Task:'), { target: { value: '1' } });
    await fireEvent.input(getByLabelText('Deadline:'), {
      target: { value: '2024-06-01T12:00' }
    });
    await fireEvent.click(getByRole('button', { name: 'Set Deadline' }));

    const errorMessage = await findByText('Server error');
    expect(errorMessage).toBeTruthy();
  });

  it('shows validation errors for empty fields', async () => {
    const { getByRole, findByText } = render(TaskDeadline, {
      props: { tasks: mockTasks }
    });

    await fireEvent.click(getByRole('button', { name: 'Set Deadline' }));

    expect(await findByText('Please select a task')).toBeTruthy();
  });
}); 