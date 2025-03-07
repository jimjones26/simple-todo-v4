<script>
  import { post } from "../utils/api.js";

  let name = "";
  let description = "";
  let error = "";
  let successMessage = "";
  let isSubmitting = false;

  async function handleSubmit(event) {
    event.preventDefault();
    error = "";
    successMessage = "";

    if (!name.trim()) {
      error = "Team name is required";
      return;
    }

    isSubmitting = true;

    try {
      const data = { name, description: description || null };
      const response = await post("/teams", data);

      successMessage = `Team "${response.name}" created successfully!`;
      name = "";
      description = "";
    } catch (err) {
      error = err.message || "Failed to create team";
    } finally {
      isSubmitting = false;
    }
  }
</script>

<form on:submit={handleSubmit}>
  <h2>Create New Team</h2>

  {#if error}
    <div class="error">{error}</div>
  {/if}

  {#if successMessage}
    <div class="success">{successMessage}</div>
  {/if}

  <div>
    <label for="name">Team Name:</label>
    <input
      id="name"
      type="text"
      bind:value={name}
      required
      aria-invalid={!!error}
      disabled={isSubmitting}
    />
  </div>

  <div>
    <label for="description">Description (optional):</label>
    <textarea id="description" bind:value={description} disabled={isSubmitting}
    ></textarea>
  </div>

  <button type="submit" disabled={isSubmitting || !name.trim()}>
    {isSubmitting ? "Creating..." : "Create Team"}
  </button>
</form>

<style>
  .error {
    color: red;
    margin-bottom: 1rem;
  }
  .success {
    color: green;
    margin-bottom: 1rem;
  }
  form {
    max-width: 400px;
    margin: 0 auto;
  }
  div {
    margin-bottom: 1rem;
  }
  input,
  textarea {
    width: 100%;
  }
  button {
    padding: 0.5rem 1rem;
  }
</style>
