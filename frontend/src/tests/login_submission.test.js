// frontend/src/tests/login_submission.test.js
import { render, fireEvent, waitFor, cleanup } from '@testing-library/svelte';
import Login from '../components/Login.svelte';
import { post } from '../utils/api';
import { vi, describe, beforeEach, afterEach, test, expect } from 'vitest';

// Mock the api module and the goto function
vi.mock('../utils/api', () => ({
  post: vi.fn(),
}));

// Mock the goto function (assuming it's part of a routing library)
const goto = vi.fn();

describe('Login Form Submission', () => {
  beforeEach(() => {
    // Reset mocks before each test
    vi.clearAllMocks();
  });

  afterEach(() => {
    cleanup();
  });

  test('test_login_form_submits_success', async () => {
    // Arrange: Mock a successful API response
    post.mockResolvedValue({ status: 'success' });

    const { getByLabelText, getByText } = render(Login);

    // Act: Fill in the form and submit
    const usernameInput = getByLabelText('Username:');
    const passwordInput = getByLabelText('Password:');
    const submitButton = getByText('Login');

    await fireEvent.input(usernameInput, { target: { value: 'testuser' } });
    await fireEvent.input(passwordInput, { target: { value: 'password' } });
    await fireEvent.click(submitButton);

    // Assert: Check if the post function was called with correct data
    await waitFor(() => {
      expect(post).toHaveBeenCalledWith('/login', {
        username: 'testuser',
        password: 'password',
      });
    });

    // Assert: Check if goto was called after successful login
    //await waitFor(() => expect(goto).toHaveBeenCalledWith('/dashboard')); //Removed as per instructions
  });

  test('test_login_form_submits_failure', async () => {
    // Arrange: Mock a failed API response
    post.mockRejectedValue(new Error('Invalid credentials')); // Simulate network or server error
    // OR, to simulate the backend's error response:
    // post.mockResolvedValue({ status: 'error', message: 'Invalid credentials' });

    const { getByLabelText, getByText, findByText } = render(Login);

    // Act: Fill in the form and submit
    const usernameInput = getByLabelText('Username:');
    const passwordInput = getByLabelText('Password:');
    const submitButton = getByText('Login');

    await fireEvent.input(usernameInput, { target: { value: 'testuser' } });
    await fireEvent.input(passwordInput, { target: { value: 'wrongpassword' } });
    await fireEvent.click(submitButton);

    // Assert: Check if the post function was called
    await waitFor(() => {
      expect(post).toHaveBeenCalledWith('/login', {
        username: 'testuser',
        password: 'wrongpassword',
      });
    });

    // Assert: Check if goto was NOT called
    expect(goto).not.toHaveBeenCalled();

    // Assert: Check if an error message is displayed (you might need to adjust this)
    await waitFor(() => {
      // Check for a generic error message.  We'll refine this in the implementation.
      expect(document.body.textContent).toContain('Invalid credentials'); //Very basic check
    });
  });
});
