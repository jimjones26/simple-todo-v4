// @ts-nocheck
import { render, fireEvent, cleanup } from '@testing-library/svelte';
import TeamForm from '../components/TeamForm.svelte';
import { post } from '../utils/api.js';
import { describe, beforeEach, test, expect, vi, afterEach } from 'vitest';

afterEach(cleanup);

vi.mock('../utils/api.js');

describe('TeamForm Submission', () => {
  beforeEach(() => {
    post.mockClear();
  });

  test('submits valid form data', async () => {
    const mockResponse = { name: 'New Team', id: 1 };
    post.mockResolvedValue(mockResponse);

    const { getByLabelText, getByRole } = render(TeamForm);

    await fireEvent.input(getByLabelText('Team Name:'), {
      target: { value: 'New Team' }
    });

    await fireEvent.click(getByRole('button', { name: /create team/i }));

    expect(post).toHaveBeenCalledWith('/teams', {
      name: 'New Team',
      description: null
    });
  });

  test('handles submission errors', async () => {
    post.mockRejectedValue(new Error('Server error'));

    const { getByLabelText, getByRole, findByText } = render(TeamForm);

    await fireEvent.input(getByLabelText('Team Name:'), {
      target: { value: 'Failing Team' }
    });

    await fireEvent.click(getByRole('button', { name: /create team/i }));

    expect(await findByText('Server error')).toBeInTheDocument();
  });
});
