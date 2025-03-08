// @ts-nocheck
import { render, fireEvent, screen, waitFor, cleanup } from '@testing-library/svelte';
import TaskStatus from '../components/TaskStatus.svelte';
import { patch } from '../utils/api.js';
import { describe, it, expect, vi, afterEach } from 'vitest';

vi.mock('../utils/api.js');

describe('TaskStatus Submission', () => {
  // Add this to clean up after each test
  afterEach(cleanup);

  it('status_form.test_submits', async () => {
    // Arrange
    const taskId = 1;
    const mockResponse = { message: 'Task status updated' };
    patch.mockResolvedValueOnce(mockResponse);

    render(TaskStatus, { taskId: taskId });

    const selectElement = screen.getByRole('combobox');
    const submitButton = screen.getByRole('button', { name: 'Update Status' });

    // Act
    await fireEvent.change(selectElement, { target: { value: 'in progress' } });
    await fireEvent.click(submitButton);

    // Assert
    expect(patch).toHaveBeenCalledWith(`/tasks/${taskId}/status`, { status: 'in progress' });

    await waitFor(() => {
      expect(screen.getByText('Status updated')).toBeInTheDocument();
    });
  });

  it('status_form.test_submission_failure', async () => {
    // Arrange
    const taskId = 1;
    patch.mockRejectedValueOnce(new Error('Failed to update status'));

    render(TaskStatus, { taskId: taskId });

    const selectElement = screen.getByRole('combobox');
    const submitButton = screen.getByRole('button', { name: 'Update Status' });

    // Act
    await fireEvent.change(selectElement, { target: { value: 'in progress' } });
    await fireEvent.click(submitButton);

    // Assert
    await waitFor(() => {
      expect(screen.getByText('Failed to update status')).toBeInTheDocument();
    });
  });
});