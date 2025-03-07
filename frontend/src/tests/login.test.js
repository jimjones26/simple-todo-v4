// @ts-nocheck
import { render, fireEvent, cleanup } from '@testing-library/svelte';
import Login from '../components/Login.svelte';
import { vi, describe, it, expect, afterEach } from 'vitest';

// Mock the API module
vi.mock('../utils/api.js', () => {
  const post = vi.fn();
  return { post };
});

describe('Login.svelte', () => {
  afterEach(() => {
    cleanup();
  });

  it('renders form with username and password fields and shows validation errors when submitted empty', async () => {
    const { getByLabelText, getByText, findByText } = render(Login);

    const usernameInput = getByLabelText('Username:');
    const passwordInput = getByLabelText('Password:');
    const submitButton = getByText('Login');

    expect(usernameInput).toBeInTheDocument();
    expect(passwordInput).toBeInTheDocument();
    expect(submitButton).toBeInTheDocument();

    await fireEvent.click(submitButton);

    const usernameError = await findByText('Username is required');
    const passwordError = await findByText('Password is required');

    expect(usernameError).toBeInTheDocument();
    expect(passwordError).toBeInTheDocument();
  });

  it('login form shows error on failed submission', async () => {
    const { post } = await import('../utils/api.js');
    post.mockResolvedValueOnce({
      ok: false,
      status: 401,
      json: async () => ({ message: 'Invalid credentials' }),
    });

    const { getByLabelText, getByText, findByText } = render(Login);
    const usernameInput = getByLabelText('Username:');
    const passwordInput = getByLabelText('Password:');
    const submitButton = getByText('Login');

    await fireEvent.input(usernameInput, { target: { value: 'testuser' } });
    await fireEvent.input(passwordInput, { target: { value: 'wrongpass' } });
    await fireEvent.click(submitButton);

    const errorMessage = await findByText('Invalid credentials');
    expect(errorMessage).toBeInTheDocument();
  });
});
