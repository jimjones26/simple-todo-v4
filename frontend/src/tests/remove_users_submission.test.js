// @ts-nocheck
import { render, fireEvent, screen, waitFor, within } from '@testing-library/svelte';
import TeamUsers from '../components/TeamUsers.svelte';
import { vi, describe, it, expect, beforeEach, afterEach } from 'vitest';
import * as api from '../utils/api';

// Mock the api module
vi.mock('../utils/api', () => ({
  post: vi.fn(),
  get: vi.fn(),
}));

describe('TeamUsers Remove Users Form Submission', () => {
  // Stub window.location with a mock reload method
  beforeEach(() => {
    vi.stubGlobal('location', {
      ...window.location, // Preserve existing properties
      reload: vi.fn(),    // Mock reload as a no-op function
    });
  });

  // Optional: Explicitly restore globals (Vitest does this automatically, but this ensures clarity)
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('test_remove_users_form_submits', async () => {
    // Mock the api.post response
    api.post.mockResolvedValue({
      message: 'Users removed successfully',
    });

    const testTeams = [{ id: 1, name: 'Team A' }];
    const testUsers = [{ id: 1, username: 'userA' }, { id: 2, username: 'userB' }];

    const { container } = render(TeamUsers, {
      props: {
        teams: testTeams,
        allUsers: testUsers,
      },
    });

    // Select team in the "Add Users" form (assuming shared state)
    const addUsersForm = container.querySelector('#team-users-form');
    const teamSelect = within(addUsersForm).getByLabelText('Team:');
    await fireEvent.change(teamSelect, { target: { value: '1' } });

    // Interact with the "Remove Users" form
    const removeUsersForm = container.querySelector('#remove-users-form');
    const userCheckbox1 = within(removeUsersForm).getByLabelText('userA');
    const userCheckbox2 = within(removeUsersForm).getByLabelText('userB');
    await fireEvent.click(userCheckbox1);
    await fireEvent.click(userCheckbox2);

    // Click the "Remove Users" button
    const removeButton = screen.getByRole('button', { name: 'Remove Users' });
    await fireEvent.click(removeButton);

    // Verify the API call
    await waitFor(() => {
      expect(api.post).toHaveBeenCalledTimes(1);
      expect(api.post).toHaveBeenCalledWith('/teams/1/users', {
        user_ids: [1, 2],
        _method: 'DELETE',
      });
    });

    // Check for success message in the DOM
    await waitFor(() => {
      expect(screen.getByText('Users removed successfully')).toBeInTheDocument();
    });

    // Verify that reload was attempted
    expect(window.location.reload).toHaveBeenCalledTimes(1);
  });
});