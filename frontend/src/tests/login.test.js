import { render, fireEvent, screen } from '@testing-library/svelte';
import Login from '../components/Login.svelte';

describe('Login component', () => {
  test('renders a form with username and password fields and validates that both are required', async () => {
    const { getByLabelText, getByRole } = render(Login);

    const usernameField = getByLabelText('Username');
    const passwordField = getByLabelText('Password');
    const submitButton = getByRole('button', { name: 'Login' });

    expect(usernameField).toBeInTheDocument();
    expect(passwordField).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();

    // Attempt to submit without filling the fields
    await fireEvent.click(submitButton);

    // Check for validation messages
    // We're anticipating that the component will display error messages with specific text
    const usernameError = await screen.findByText('Username is required');
    const passwordError = await screen.findByText('Password is required');

    expect(usernameError).toBeInTheDocument();
    expect(passwordError).toBeInTheDocument();
  });
});
