// frontend/src/tests/remove_users_submission.test.js
import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import TeamUsers from '../components/TeamUsers.svelte';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as api from '../utils/api';

describe('TeamUsers Remove Users Form Submission', () => {
  beforeEach(() => {
    api.post = vi.fn(); // Mock the post function
    api.get = vi.fn();
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('test_remove_users_form_submits', async () => {
    const mockDelete = vi.fn().mockResolvedValue({
      ok: true,
      json: () => Promise.resolve({ message: 'Users removed successfully' }),
    });
    global.fetch.mockImplementation(mockDelete);

    const testTeams = [{ id: 1, name: 'Team A' }];
    const testUsers = [{ id: 1, username: 'userA' }, { id: 2, username: 'userB' }];

    const { component } = render(TeamUsers, {
      props: {
        teams: testTeams,
        allUsers: testUsers,
      },
    });

    const teamSelect = screen.getByLabelText('Team:');
    await fireEvent.change(teamSelect, { target: { value: '1' } });

    const userCheckbox1 = screen.getByLabelText('userA');
    const userCheckbox2 = screen.getByLabelText('userB');
    await fireEvent.click(userCheckbox1);
    await fireEvent.click(userCheckbox2);

    const removeButton = screen.getByRole('button', { name: 'Remove Users' });
    await fireEvent.click(removeButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(global.fetch).toHaveBeenCalledWith('/teams/1/users', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_ids: [1, 2] }),
      });
    });

    // Optionally check for success message
    await waitFor(() => {
      expect(screen.getByText('Users removed successfully')).toBeInTheDocument();
    });
  });
});
