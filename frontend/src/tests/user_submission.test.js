import { render, fireEvent, screen, waitFor } from '@testing-library/svelte';
import UserForm from '../components/UserForm.svelte';
import * as api from '../utils/api';
import { vi, describe, expect, test } from 'vitest';

// Mock the api.post function
vi.mock('../utils/api', () => {
  return {
    post: vi.fn(),
  };
});

describe('UserForm submission', () => {
  test('submits the form with valid data and handles a 201 response', async () => {
    // Arrange
    // @ts-ignore
    const mockPost = api.post.mockResolvedValueOnce({ id: 1, username: 'testuser', role: 'admin' });

    render(UserForm);

    const usernameInput = screen.getByLabelText('Username:');
    const emailInput = screen.getByLabelText('Email:');
    const passwordInput = screen.getByLabelText('Password:');
    const roleInput = screen.getByLabelText('Role:');
    const submitButton = screen.getByText('Create User');

    // Act
    await fireEvent.input(usernameInput, { target: { value: 'testuser' } });
    await fireEvent.input(emailInput, { target: { value: 'test@example.com' } });
    await fireEvent.input(passwordInput, { target: { value: 'password' } });
    await fireEvent.input(roleInput, { target: { value: 'admin' } });
    await fireEvent.click(submitButton);

    // Assert
    await waitFor(() => {
      expect(api.post).toHaveBeenCalledTimes(1);
      expect(api.post).toHaveBeenCalledWith('/users', {
        username: 'testuser',
        email: 'test@example.com',
        password: 'password',
        role: 'admin',
      });
    });
  });
});
