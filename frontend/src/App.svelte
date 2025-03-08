<script>
  import { onMount } from "svelte";
  import { auth, checkAuth } from "./stores/authStore";
  import Login from "./components/Login.svelte";
  import UserForm from "./components/UserForm.svelte";
  import Dashboard from "./components/Dashboard.svelte";
  import TeamForm from "./components/TeamForm.svelte";
  import { logout, get } from "./utils/api";
  import TeamUsers from "./components/TeamUsers.svelte";
  import TaskForm from "./components/TaskForm.svelte";
  import TaskAssign from "./components/TaskAssign.svelte";
  import UserTasks from "./components/UserTasks.svelte";
  import TaskDeadline from "./components/TaskDeadline.svelte";

  let logoutError = "";
  let teams = [];
  let allUsers = [];

  onMount(async () => {
    await checkAuth();
    if ($auth.isAuthenticated && $auth.user?.role === "admin") {
      try {
        const teamsResponse = await get("/teams");
        const usersResponse = await get("/users");
        teams = teamsResponse;
        allUsers = usersResponse;
      } catch (error) {
        console.error("Error fetching ", error);
      }
    }
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
    <Dashboard on:logout={handleLogout} user={$auth.user} {logoutError} />
    <TeamForm />
    <TeamUsers {teams} {allUsers} />
    <TaskForm {teams} />
    <TaskDeadline />
    <TaskAssign task={""} users={""} />
    <UserTasks />
  {/if}

  {#if !$auth.isAuthenticated}
    <Login />
  {/if}
{/if}

<UserForm />

{JSON.stringify({ auth: $auth }, null, 2)}

<style>
</style>
