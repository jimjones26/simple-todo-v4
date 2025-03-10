import { render, fireEvent, cleanup, waitFor } from '@testing-library/svelte';
import TeamForm from '../components/TeamForm.svelte';
import { describe, test, expect, afterEach } from 'vitest';

afterEach(cleanup);

describe('TeamForm Component', () => {
  test('renders form elements', async () => {
    const { getByLabelText, getByRole } = render(TeamForm);

    expect(getByLabelText('Team Name:')).toBeInTheDocument();
    expect(getByLabelText('Description (optional):')).toBeInTheDocument();
    expect(getByRole('button', { name: /create team/i })).toBeInTheDocument();
  });

  test('shows validation error for empty name', async () => {
    const { container, getByText } = render(TeamForm);
    const form = container.querySelector('form');

    await fireEvent.submit(form);
    await waitFor(() => expect(getByText('Team name is required')).toBeInTheDocument());
  });

  test('enables button with valid input', async () => {
    const { getByRole, getByLabelText } = render(TeamForm);
    const input = getByLabelText('Team Name:');
    const button = getByRole('button', { name: /create team/i });

    await fireEvent.input(input, { target: { value: 'Dev Team' } });
    expect(button).not.toBeDisabled();
  });
});
