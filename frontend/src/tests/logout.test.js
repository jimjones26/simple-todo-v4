// frontend/src/tests/logout.test.js
import { render, screen, fireEvent } from '@testing-library/svelte';
import Dashboard from '../components/Dashboard.svelte';
import { vi, describe, expect, test } from 'vitest';

describe('Dashboard Component', () => {
  test('should render the logout button', async () => {
    // Provide a mock user prop to prevent the TypeError
    render(Dashboard, { props: { user: { username: 'testuser' }, logoutError: '' } });
    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
  });

  test('should dispatch the logout event when the logout button is clicked', async () => {
    // Render with user prop and get the component instance
    const { component } = render(Dashboard, { props: { user: { username: 'testuser' }, logoutError: '' } });
    const mockLogout = vi.fn();
    // Listen for the 'logout' event
    component.on('logout', mockLogout);
    const logoutButton = screen.getByRole('button', { name: /logout/i });
    await fireEvent.click(logoutButton);
    // Verify the event was dispatched
    expect(mockLogout).toHaveBeenCalledTimes(1);
  });
});
