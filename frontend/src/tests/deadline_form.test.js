import { render, cleanup } from '@testing-library/svelte';
import { describe, it, afterEach, expect } from 'vitest';
import TaskDeadline from '../components/TaskDeadline.svelte';

describe('TaskDeadline Component', () => {
  afterEach(() => {
    cleanup();
  });

  const mockTasks = [
    { id: 1, title: 'Task 1' },
    { id: 2, title: 'Task 2' }
  ];

  it('renders form with task selection and deadline inputs', () => {
    const { getByLabelText, getByRole } = render(TaskDeadline, {
      props: { tasks: mockTasks }
    });

    // Verify form structure
    expect(getByRole('form')).toBeTruthy();
    
    // Task selection elements
    expect(getByLabelText('Task:')).toBeTruthy();
    const select = getByLabelText('Task:');
    expect(select.tagName).toBe('SELECT');
    expect(select.children.length).toBe(mockTasks.length + 1); // Options + default

    // Deadline input
    expect(getByLabelText('Deadline:')).toBeTruthy();
    const dateInput = getByLabelText('Deadline:');
    expect(dateInput.type).toBe('datetime-local');

    // Submit button
    expect(getByRole('button', { name: 'Set Deadline' })).toBeTruthy();
  });

  it('populates task dropdown with provided tasks', () => {
    const { getByLabelText } = render(TaskDeadline, { 
      props: { tasks: mockTasks }
    });
    
    const options = getByLabelText('Task:').querySelectorAll('option');
    expect(options.length).toBe(mockTasks.length + 1); // Includes default
    mockTasks.forEach((task, index) => {
      expect(options[index + 1].textContent).toBe(task.title);
    });
  });
});
