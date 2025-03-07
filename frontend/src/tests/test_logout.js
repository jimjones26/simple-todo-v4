// frontend/src/tests/test_logout.js
import { render, screen, fireEvent } from '@testing-library/svelte';
import Dashboard from '../components/Dashboard.svelte';
import * as api from '../utils/api';

// Mock the logout function from api.js
jest.mock('../utils/api', () => ({
  logout: jest.fn().mockResolvedValue({ message: 'Logged out successfully' }),
}));

describe('Dashboard Component', () => {
  test('should render the logout button', async () => {
    render(Dashboard);
    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    expect(logoutButton).toBeInTheDocument();
  });

  test('should call the logout function when the logout button is clicked', async () => {
    render(Dashboard);
    const logoutButton = await screen.findByRole('button', { name: /logout/i });
    
    // Simulate a click event
    await fireEvent.click(logoutButton);

    // Wait for the logout function to be called
    expect(api.logout).toHaveBeenCalledTimes(1);
  });
});
