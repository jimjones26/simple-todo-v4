import { render, fireEvent, cleanup } from '@testing-library/svelte';
import Login from '../components/Login.svelte';
import { describe, it, expect, afterEach } from 'vitest';

describe('Login.svelte', () => {
  afterEach(() => {
    cleanup(); // Clean up after each test, matching the working test
  });

  it('renders form with username and password fields and shows validation errors when submitted empty', async () => {
    // Render the component and get query functions, like the working test
    const { getByLabelText, getByText, findByText } = render(Login);

    // Query form elements, similar to getByLabelText and getByText in the working test
    const usernameInput = getByLabelText('Username');
    const passwordInput = getByLabelText('Password');
    const submitButton = getByText('Login');

    // Assert fields and button are rendered, using toBeInTheDocument like the working test implies
    expect(usernameInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();

    // Simulate clicking the submit button without input, mirroring fireEvent usage
    await fireEvent.click(submitButton);

    // Check for validation errors, using findByText for async DOM updates
    const usernameError = await findByText('Username is required');
    const passwordError = await findByText('Password is required');

    // Assert errors are in the document, consistent with testing-library style
    expect(usernameError).toBeInTheDocument();
    expect(passwordError).toBeInTheDocument();
  });
});