<script>
  export let task;
  export let users;

  let selectedUser = '';
  let errorMessage = '';
  let successMessage = '';
  let isSubmitting = false;

  async function handleAssign() {
    errorMessage = '';
    successMessage = '';

    if (!selectedUser) {
      errorMessage = 'Please select a user.';
      return;
    }

    isSubmitting = true;
    try {
      const response = await fetch(`http://127.0.0.1:5001/tasks/${task.id}/assign`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: selectedUser }),
        credentials: 'include',
      });

      if (!response.ok) {
        const errorBody = await response.json();
        errorMessage = errorBody.message || 'Failed to assign user.';
        return;
      }

      successMessage = 'User assigned successfully!';
    } catch (error) {
      errorMessage = error.message || 'An unexpected error occurred.';
    } finally {
      isSubmitting = false;
    }
  }
</script>

{#if errorMessage}
  <p style="color: red">{errorMessage}</p>
{/if}

{#if successMessage}
  <p style="color: green">{successMessage}</p>
{/if}

<div>
  <label for="user">Select user:</label>
  <select id="user" bind:value={selectedUser} disabled={isSubmitting}>
    <option value="">-- Select a user --</option>
    {#each users as user (user.id)}
      <option value={user.id}>{user.username}</option>
    {/each}
  </select>
</div>

<button on:click={handleAssign} disabled={isSubmitting}>
  {isSubmitting ? 'Assigning...' : 'Assign'}
</button>
