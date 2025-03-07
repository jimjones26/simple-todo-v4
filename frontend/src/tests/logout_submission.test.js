// frontend/src/tests/logout_submission.test.js
import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import Wrapper from './Wrapper.svelte'; // Import the wrapper
import { vi, describe, test, expect } from 'vitest';
import * as api from '../utils/api';

vi.mock('../utils/api');

describe('Dashboard Component - Logout Submission', () => {
  test('clicking logout button triggers API call and redirects to login', async () => {
    // Mock the logout function from the api module
    api.logout = vi.fn().mockResolvedValue({ message: 'Logged out successfully' });

    // Mock window.location.assign
    const assignMock = vi.fn();
    vi.stubGlobal('location', { ...window.location, assign: assignMock });

    // Render the wrapper component with the logout handler
    render(Wrapper, {
      props: {
        handleLogout: async () => {
          await api.logout();
          window.location.assign('/login');
        },
      },
    });

    // Find the logout button
    const logoutButton = await screen.findByRole('button', { name: /logout/i });

    // Click the logout button
    await fireEvent.click(logoutButton);

    // Verify that the logout API function was called
    await waitFor(() => {
      expect(api.logout).toHaveBeenCalled();
    });

    // Verify that the redirect happened
    await waitFor(() => {
      expect(assignMock).toHaveBeenCalledWith('/login');
    });
  });
});