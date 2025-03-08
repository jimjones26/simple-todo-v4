import { render, screen, cleanup } from '@testing-library/svelte';
import TaskAssign from '../components/TaskAssign.svelte';
import { describe, it, expect, afterEach } from 'vitest';

describe('TaskAssign.svelte', () => {
  afterEach(() => {
    cleanup();
  });

  it('renders the component', () => {
    const { container } = render(TaskAssign, {
      props: {
        task: { id: 1, title: 'Test Task' },
        users: [
          { id: 1, username: 'User 1' },
          { id: 2, username: 'User 2' },
        ],
      },
    });

    expect(container).toBeInTheDocument();
  });

  it('renders the user selection dropdown', () => {
    render(TaskAssign, {
      props: {
        task: { id: 1, title: 'Test Task' },
        users: [
          { id: 1, username: 'User 1' },
          { id: 2, username: 'User 2' },
        ],
      },
    });

    const selectElement = screen.getByLabelText('Select user:');
    expect(selectElement).toBeInTheDocument();

    const option1 = screen.getByText('User 1');
    expect(option1).toBeInTheDocument();

    const option2 = screen.getByText('User 2');
    expect(option2).toBeInTheDocument();
  });

  it('renders the assign button', () => {
    render(TaskAssign, {
      props: {
        task: { id: 1, title: 'Test Task' },
        users: [
          { id: 1, username: 'User 1' },
          { id: 2, username: 'User 2' },
        ],
      },
    });

    const assignButton = screen.getByText('Assign');
    expect(assignButton).toBeInTheDocument();
  });
});
