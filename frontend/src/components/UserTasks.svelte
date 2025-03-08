<script>
  import { onMount } from 'svelte';
  import { get } from '../utils/api';
  import { auth } from '../stores/authStore';

  let tasks = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const user = $auth.user;
      if (!user) {
        error = 'User not logged in.';
        loading = false;
        return;
      }
      tasks = await get(`/users/${user.id}/tasks`);
      loading = false;
    } catch (err) {
      error = err.message || 'Failed to fetch tasks.';
      loading = false;
    }
  });
</script>

<h2>My Tasks</h2>

{#if loading}
  <p>Loading tasks...</p>
{:else if error}
  <p class="error">Error: {error}</p>
{:else if tasks.length === 0}
  <p>No tasks assigned.</p>
{:else}
  <ul>
    {#each tasks as task (task.id)}
      <li>
        <h3>{task.title}</h3>
        <p>{task.description}</p>
        <p>Status: {task.status}</p>
        {#if task.deadline}
          <p>Deadline: {task.deadline}</p>
        {/if}
        <!-- You might want to display team information here too -->
      </li>
    {/each}
  </ul>
{/if}

<style>
    .error {
        color: red;
    }
</style>
