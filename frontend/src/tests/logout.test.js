// frontend/src/tests/logout.test.js
import { render, screen, fireEvent, cleanup } from '@testing-library/svelte';
import Wrapper from './Wrapper.svelte';
import { describe, test, expect, vi, afterEach } from 'vitest';

afterEach(cleanup);

describe('Dashboard Component', () => {
  test('should render the logout button', async () => {
    render(Wrapper, { props: { user: { username: 'testuser' }, logoutError: '' } });
    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
  });

  test('should dispatch the logout event when the logout button is clicked', async () => {
    const mockLogout = vi.fn();
    render(Wrapper, {
      props: {
        handleLogout: mockLogout,
      },
    });
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    await fireEvent.click(logoutButton);
    expect(mockLogout).toHaveBeenCalledTimes(1);
  });
});