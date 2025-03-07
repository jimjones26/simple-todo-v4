<!-- src/tests/Wrapper.svelte -->
<script>
  import Dashboard from "../components/Dashboard.svelte";

  export let handleLogout;
  let user = { username: "testuser" };
  let logoutError = "";
</script>

<Dashboard {user} {logoutError} on:logout={handleLogout} />
