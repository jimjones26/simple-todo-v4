// @ts-nocheck
import { cleanup, render, screen, fireEvent, within } from '@testing-library/svelte';
import TeamUsers from '../components/TeamUsers.svelte';
import { post } from '../utils/api';
import { describe, it, afterEach, vi, expect } from 'vitest';

vi.mock('../utils/api.js');

const testTeams = [
  { id: 1, name: 'Dev Team' },
  { id: 2, name: 'QA Team' },
];

const testUsers = [
  { id: 11, username: 'userA' },
  { id: 22, username: 'userB' },
];

describe('TeamUsers Form Submission', () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it('submits selected team and users to API', async () => {
    post.mockResolvedValue({ ok: true });

    const { container } = render(TeamUsers, {
      props: { teams: testTeams, allUsers: testUsers },
    });

    const addUsersForm = container.querySelector('#team-users-form');
    await fireEvent.change(within(addUsersForm).getByLabelText(/Team:/), { target: { value: '1' } });
    await fireEvent.click(within(addUsersForm).getByLabelText('userA'));
    await fireEvent.click(within(addUsersForm).getByLabelText('userB'));
    await fireEvent.click(screen.getByRole('button', { name: /Add Users/i }));

    expect(post).toHaveBeenCalledWith('/teams/1/users', { user_ids: [11, 22] });
  });

  it('shows error message on API failure', async () => {
    post.mockResolvedValue({
      ok: false,
      status: 500,
      json: () => Promise.resolve({ message: 'Error adding users' }),
    });

    const { container } = render(TeamUsers, {
      props: { teams: testTeams, allUsers: testUsers },
    });

    const addUsersForm = container.querySelector('#team-users-form');
    await fireEvent.change(within(addUsersForm).getByLabelText(/Team:/), { target: { value: '2' } });
    await fireEvent.click(within(addUsersForm).getByLabelText('userA'));
    await fireEvent.click(screen.getByRole('button', { name: /Add Users/i }));

    expect(await screen.findByText(/Error adding users/i)).toBeInTheDocument();
  });
});