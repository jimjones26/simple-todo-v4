import { render, fireEvent, screen, cleanup } from '@testing-library/svelte';
import TaskForm from '../components/TaskForm.svelte';
import { describe, it, expect, afterEach } from 'vitest';

describe('TaskForm.svelte', () => {
  afterEach(() => {
    cleanup();
  });

  it('renders form elements', () => {
    render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    expect(screen.getByLabelText('Title:')).toBeInTheDocument();
    expect(screen.getByLabelText('Description:')).toBeInTheDocument();
    expect(screen.getByLabelText('Team:')).toBeInTheDocument();
    expect(screen.getByText('Create Task')).toBeInTheDocument();
  });

  it('shows error message when submitting empty form', async () => {
    render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    const submitButton = screen.getByText('Create Task');
    await fireEvent.click(submitButton);

    expect(screen.getByText('Title is required')).toBeInTheDocument();
    expect(screen.getByText('Team is required')).toBeInTheDocument();
  });

  it('does not show error messages initially', () => {
    render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    expect(screen.queryByText('Title is required')).not.toBeInTheDocument();
    expect(screen.queryByText('Team is required')).not.toBeInTheDocument();
  });
});