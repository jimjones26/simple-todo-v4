<script>
  import { post } from '../utils/api';
  import { auth } from '../stores/authStore';

  let username = '';
  let password = '';
  let error = '';

  async function handleSubmit() {
    error = '';
    try {
      const response = await post('/login', { username, password }); // Use POST to /login
      // Assuming the backend returns user data on successful login
      auth.set({ isAuthenticated: true, user: response, isLoading: false }); // Update auth store
    } catch (err) {
      console.error("Login failed:", err);
      error = 'Invalid credentials. Please try again.'; // More user-friendly error
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} required />
  </div>
  <div>
    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} required />
  </div>
  <button type="submit">Login</button>
  {#if error}
    <p class="error">{error}</p>
  {/if}
</form>

<style>
  .error {
    color: red;
  }
</style>
