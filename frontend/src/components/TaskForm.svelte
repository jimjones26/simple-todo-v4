<script>
  import { post } from '../utils/api.js';

  export let teams = [];

  let title = '';
  let description = '';
  let team_id = '';

  let titleError = '';
  let teamError = '';
  let submissionError = '';
  let submissionSuccess = false;
  let isSubmitting = false;

  async function handleSubmit(event) {
    event.preventDefault();
    submissionError = '';
    submissionSuccess = false;

    if (!validateForm()) {
      return;
    }

    isSubmitting = true;

    try {
      const taskData = { title, description, team_id };
      const response = await post('/tasks', taskData);
      submissionSuccess = true;
      title = '';
      description = '';
      team_id = '';
    } catch (error) {
      submissionError = error.message || 'An unexpected error occurred.';
    } finally {
      isSubmitting = false;
    }
  }

  function validateForm() {
    titleError = title ? '' : 'Title is required';
    teamError = team_id ? '' : 'Team is required';
    return !titleError && !teamError;
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <h2>Create New Task</h2>

  {#if submissionSuccess}
    <p class="success">Task created successfully!</p>
  {/if}

  {#if submissionError}
    <p class="error">{submissionError}</p>
  {/if}

  <div>
    <label for="title">Title:</label>
    <input type="text" id="title" bind:value={title} />
    {#if titleError}
      <p class="error">{titleError}</p>
    {/if}
  </div>

  <div>
    <label for="description">Description:</label>
    <textarea id="description" bind:value={description} />
  </div>

  <div>
    <label for="team">Team:</label>
    <select id="team" bind:value={team_id}>
      <option value="">Select a team</option>
      {#each teams as team (team.id)}
        <option value={team.id}>{team.name}</option>
      {/each}
    </select>
    {#if teamError}
      <p class="error">{teamError}</p>
    {/if}
  </div>

  <button type="submit" disabled={isSubmitting}>
    {isSubmitting ? 'Creating...' : 'Create Task'}
  </button>
</form>

<style>
  .error {
    color: red;
  }
  .success {
    color: green;
  }
</style>
