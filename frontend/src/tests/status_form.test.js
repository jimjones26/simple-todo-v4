import { render, screen } from '@testing-library/svelte';
import TaskStatus from '../components/TaskStatus.svelte';
import { describe, it, expect, vi } from 'vitest';

describe('TaskStatus.svelte', () => {
  it('status_form.test_renders', async () => {
    render(TaskStatus);

    // Check for the select element
    const selectElement = screen.getByRole('combobox');
    expect(selectElement).toBeInTheDocument();

    // Check for the options
    const notStartedOption = screen.getByText('not started');
    const inProgressOption = screen.getByText('in progress');
    const completedOption = screen.getByText('completed');

    expect(notStartedOption).toBeInTheDocument();
    expect(inProgressOption).toBeInTheDocument();
    expect(completedOption).toBeInTheDocument();

    // Check for the submit button
    const submitButton = screen.getByRole('button', { name: 'Update Status' });
    expect(submitButton).toBeInTheDocument();
  });
});
