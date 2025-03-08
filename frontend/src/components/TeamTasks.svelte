<!-- frontend/src/components/TeamTasks.svelte -->
<script>
  import { onMount } from 'svelte';
  import { get } from '../utils/api';

  export let teamId;

  let tasks = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      tasks = await get(`/teams/${teamId}/tasks`);
    } catch (err) {
      error = err.message || 'Failed to fetch tasks.';
    } finally {
      loading = false;
    }
  });
</script>

<h1>Team Tasks</h1>

{#if loading}
  <p>Loading tasks...</p>
{:else if error}
  <p class="error">Error: {error}</p>
{:else if tasks.length === 0}
  <p>No tasks for this team.</p>
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
      </li>
    {/each}
  </ul>
{/if}

<style>
    .error {
        color: red;
    }
</style>
