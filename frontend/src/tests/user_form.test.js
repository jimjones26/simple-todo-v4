import { render, fireEvent, cleanup } from '@testing-library/svelte';
import UserForm from '../components/UserForm.svelte';
import { describe, it, expect, vi, afterEach } from 'vitest';
import { post } from '../utils/api';

// Mock the post function to return a resolved promise
vi.mock('../utils/api', () => ({
  post: vi.fn().mockResolvedValue({}),
}));

describe('UserForm.svelte', () => {
  afterEach(() => {
    cleanup();
  });

  it('calls the post function with user data when the form is valid', async () => {
    const { getByLabelText, getByText } = render(UserForm); // No onSubmit prop needed

    const usernameInput = getByLabelText('Username:');
    const emailInput = getByLabelText('Email:');
    const passwordInput = getByLabelText('Password:');
    const roleInput = getByLabelText('Role:');
    const submitButton = getByText('Create User');

    await fireEvent.input(usernameInput, { target: { value: 'testuser' } });
    await fireEvent.input(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'password123' } });
    await fireEvent.input(roleInput, { target: { value: 'admin' } });
    await fireEvent.click(submitButton);

    expect(post).toHaveBeenCalledWith('/users', {
      username: 'testuser',
      email: 'test@example.com',
      password: 'password123',
      role: 'admin',
    });
  });
});