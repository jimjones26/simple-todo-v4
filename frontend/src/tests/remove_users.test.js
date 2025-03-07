import { render } from '@testing-library/svelte';
import TeamUsers from '../components/TeamUsers.svelte';

describe('TeamUsers.svelte', () => {
  it('test_remove_users_form_renders', () => {
    const { getByText } = render(TeamUsers, {
      props: {
        teams: [{ id: 1, name: 'Team A' }],
        allUsers: [{ id: 1, username: 'userA' }, { id: 2, username: 'userB' }],
      },
    });

    // Check if the "Remove Users" button is rendered
    expect(() => getByText('Remove Users')).not.toThrow();
  });
});
