<script>
  // frontend/src/App.svelte
  import { onMount } from 'svelte';
  import { auth, checkAuth } from './stores/authStore'; // Import the store and checkAuth
  import Login from './components/Login.svelte'; // Import your Login component
  import { logout } from './utils/api'; // Import the logout function
  let logoutError = ''; // Add a variable to store logout errors

  // Call checkAuth when the component mounts
  onMount(async () => {
    await checkAuth();
  });

  async function handleLogout() {
      logoutError = ''; // Clear any previous error
      try {
          await logout(); // Call the logout function from api.js
          auth.set({ isAuthenticated: false, user: null, isLoading: false }); // Update the store
      } catch (error) {
          console.error("Logout failed:", error);
          logoutError = 'Logout failed. Please try again.'; // Set a user-friendly error message
      }
  }
</script>

{#if $auth.isLoading}
  <p>Loading...</p>
{:else}
  {#if $auth.isAuthenticated}
    <p>What's up, {$auth.user.username}!</p>
    <button on:click={handleLogout}>Logout</button>
    {#if logoutError}
      <p class="error">{logoutError}</p>
    {/if}
  {/if}

  {#if !$auth.isAuthenticated}
      <Login />
  {/if}
{/if}
<style>
  .error {
    color: red;
  }
</style>
