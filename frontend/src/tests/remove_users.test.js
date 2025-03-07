import { render, screen } from '@testing-library/svelte';
import TeamUsers from '../components/TeamUsers.svelte';
import { describe, it, expect } from 'vitest';

describe('TeamUsers.svelte', () => {
  it('renders the Remove Users form', () => {
    render(TeamUsers, {
      props: {
        teams: [{ id: 1, name: 'Team A' }],
        allUsers: [{ id: 1, username: 'userA' }, { id: 2, username: 'userB' }],
      },
    });

    expect(screen.getByRole('button', { name: /Remove Users/i })).toBeInTheDocument();
  });
});