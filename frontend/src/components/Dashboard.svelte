<!-- frontend/src/components/Dashboard.svelte -->
<script>
  import { createEventDispatcher } from "svelte";

  const dispatch = createEventDispatcher();

  function handleLogout() {
    dispatch("logout");
  }

  export let user, logoutError;
</script>

<div>
  <h1>Dashboard</h1>
  <p>What's up, {user.username}!</p>
  <button type="button" on:click={handleLogout}>Logout</button>
  {#if logoutError}
    <p class="error">{logoutError}</p>
  {/if}
</div>
