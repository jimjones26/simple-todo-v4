import { render, fireEvent, screen } from '@testing-library/svelte';
import TaskForm from '../components/TaskForm.svelte';

describe('TaskForm.svelte', () => {
  it('renders form elements', () => {
    const { getByLabelText, getByText } = render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    expect(getByLabelText('Title:')).toBeInTheDocument();
    expect(getByLabelText('Description:')).toBeInTheDocument();
    expect(getByLabelText('Team:')).toBeInTheDocument();
    expect(getByText('Create Task')).toBeInTheDocument();
  });

  it('shows error message when submitting empty form', async () => {
    const { getByText } = render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    const submitButton = getByText('Create Task');
    await fireEvent.click(submitButton);

    expect(getByText('Title is required')).toBeInTheDocument();
    expect(getByText('Team is required')).toBeInTheDocument();
  });

  it('does not show error messages initially', () => {
    const { queryByText } = render(TaskForm, {
      props: { teams: [{ id: 1, name: 'Team 1' }] },
    });

    expect(queryByText('Title is required')).not.toBeInTheDocument();
    expect(queryByText('Team is required')).not.toBeInTheDocument();
  });
});
