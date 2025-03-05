import { render, fireEvent } from '@testing-library/svelte';
import UserForm from '../components/UserForm.svelte';
import { describe, expect, it } from 'vitest';

describe('UserForm.svelte', () => {
  it('renders input fields for username, email, password, and role', () => {
    const { getByLabelText } = render(UserForm);

    expect(getByLabelText('Username:')).toBeInTheDocument();
    expect(getByLabelText('Email:')).toBeInTheDocument();
    expect(getByLabelText('Password:')).toBeInTheDocument();
    expect(getByLabelText('Role:')).toBeInTheDocument();
  });

  it('displays validation errors for invalid inputs', async () => {
    const { getByText, getByLabelText } = render(UserForm);

    const usernameInput = getByLabelText('Username:');
    const emailInput = getByLabelText('Email:');
    const passwordInput = getByLabelText('Password:');
    const roleInput = getByLabelText('Role:');
    const submitButton = getByText('Create User');

    // Trigger validation errors by submitting empty form
    await fireEvent.click(submitButton);

    expect(getByText('Username is required')).toBeInTheDocument();
    expect(getByText('Email is required')).toBeInTheDocument();
    expect(getByText('Password is required')).toBeInTheDocument();
    expect(getByText('Role is required')).toBeInTheDocument();

    // Enter an invalid email
    await fireEvent.input(emailInput, { target: { value: 'invalid-email' } });
    await fireEvent.click(submitButton);

    expect(getByText('Invalid email address')).toBeInTheDocument();
  });
});
