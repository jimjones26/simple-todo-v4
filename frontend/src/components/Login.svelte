<script>
  import { post } from '../utils/api';
  import { auth } from '../stores/authStore'; // Import the auth store

  let username = '';
  let password = '';
  let usernameError = '';
  let passwordError = '';
  let errorMessage = ''; // Add a variable to store the error message

  async function handleSubmit() { // Make the function async
    usernameError = username ? '' : 'Username is required';
    passwordError = password ? '' : 'Password is required';
    errorMessage = ''; // Reset error message on each submit attempt

    if (usernameError || passwordError) {
      return; // Prevent submission if there are errors
    }

    try {
      const response = await post('/login', { username, password });

      if (response.status === 'success') {
        // Update the auth store on successful login.  This will
        // automatically cause App.svelte to re-render, showing the
        // logged-in view.  No explicit navigation is needed.
        auth.update(current => {
          return { ...current, isAuthenticated: true, user: { username: username } }; // Update user info as needed
        });
      } else {
        // Handle the case where the backend returns an error status
        errorMessage = response.message || 'An unexpected error occurred.';
      }
    } catch (error) {
      // Handle network errors or errors thrown by handleResponse
      errorMessage = error.message || 'An unexpected error occurred.';
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="username">Username</label>
    <input type="text" id="username" bind:value={username} />
    {#if usernameError}
      <p class="error">{usernameError}</p>
    {/if}
  </div>

  <div>
    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} />
    {#if passwordError}
      <p class="error">{passwordError}</p>
    {/if}
  </div>

  {#if errorMessage}
    <p class="error">{errorMessage}</p>
  {/if}

  <button type="submit">Login</button>
</form>

<style>
  .error {
    color: red;
  }
</style>
