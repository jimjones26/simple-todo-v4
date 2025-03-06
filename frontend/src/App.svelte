<script>
  import { onMount } from "svelte";
  import { auth, checkAuth } from "./stores/authStore";
  import Login from "./components/Login.svelte";
  import UserForm from "./components/UserForm.svelte";
  import { logout } from "./utils/api";
  let logoutError = "";

  // Call checkAuth when the component mounts
  onMount(async () => {
    await checkAuth();
  });

  async function handleLogout() {
    logoutError = "";
    try {
      await logout();
      auth.set({ isAuthenticated: false, user: null, isLoading: false });
    } catch (error) {
      console.error("Logout failed:", error);
      logoutError = "Logout failed. Please try again.";
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

<UserForm />

{JSON.stringify({auth: $auth}, null, 2)}

<style>
  .error {
    color: red;
  }
</style>
