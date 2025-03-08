<script>
  import { patch } from "../utils/api.js"; // Add this import

  export let tasks = [];

  let task_id = "";
  let deadline = "";
  let submissionError = "";
  let submissionSuccess = false;
  let isSubmitting = false;

  async function handleSubmit(event) {
    // Make async
    event.preventDefault();
    submissionError = "";
    submissionSuccess = false;

    // Validation
    if (!task_id) {
      submissionError = "Please select a task";
      return;
    }
    if (!deadline) {
      submissionError = "Please select a deadline";
      return;
    }

    isSubmitting = true;

    try {
      // Format deadline for API
      const isoDeadline = new Date(deadline).toISOString();

      // Call API endpoint
      await patch(`/tasks/${task_id}/deadline`, {
        deadline: isoDeadline,
      });

      // Reset form on success
      task_id = "";
      deadline = "";
      submissionSuccess = true;
    } catch (error) {
      submissionError = error.message || "Failed to update deadline";
    } finally {
      isSubmitting = false;
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit} aria-labelledby="form-title">
  <h2>Set Task Deadline</h2>

  {#if submissionSuccess}
    <p class="success">Deadline updated successfully!</p>
  {/if}

  {#if submissionError}
    <p class="error">{submissionError}</p>
  {/if}

  <div>
    <label for="task">Task:</label>
    <select id="task" bind:value={task_id} disabled={isSubmitting}>
      <option value="">Select a task</option>
      {#each tasks as task (task.id)}
        <option value={task.id}>{task.title}</option>
      {/each}
    </select>
  </div>

  <div>
    <label for="deadline">Deadline:</label>
    <input
      type="datetime-local"
      id="deadline"
      bind:value={deadline}
      disabled={isSubmitting}
    />
  </div>

  <button type="submit" disabled={isSubmitting}>
    {isSubmitting ? "Setting Deadline..." : "Set Deadline"}
  </button>
</form>

<style>
  form {
    max-width: 500px;
    margin: 20px auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  div {
    margin-bottom: 15px;
  }
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }
  select,
  input[type="datetime-local"] {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  button {
    background-color: #4caf50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
  }
  .error {
    color: #ff4444;
    margin-top: 10px;
  }
  .success {
    color: #00c851;
    margin-top: 10px;
  }
</style>
