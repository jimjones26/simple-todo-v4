// frontend/src/tests/test_logout_submission.js
import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import Dashboard from '../components/Dashboard.svelte';
import { vi, describe, test } from 'vitest';
import * as api from '../utils/api';

vi.mock('../utils/api');

describe('Dashboard Component - Logout Submission', () => {
  test('clicking logout button triggers API call and redirects to login', async () => {
    // Mock the logout function from the api module
    api.logout = vi.fn().mockResolvedValue({ message: 'Logged out successfully' });

    // Mock window.location.assign
    const assignMock = vi.fn();
    delete window.location;
    window.location = { assign: assignMock };

    render(Dashboard);

    // Find the logout button
    const logoutButton = await screen.findByRole('button', { name: /logout/i });

    // Click the logout button
    await fireEvent.click(logoutButton);

    // Verify that the logout API function was called
    expect(api.logout).toHaveBeenCalled();

    // Wait for the redirection to happen.  We use waitFor to handle the asynchronous
    // nature of the redirect.
    await waitFor(() => {
      expect(assignMock).toHaveBeenCalledWith('/login');
    });
  });
});
