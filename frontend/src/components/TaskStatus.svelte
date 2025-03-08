<script>
    import { patch } from "../utils/api.js";

    export let taskId;
    let selectedStatus = "not started"; // Default status
    let submissionError = null;
    let submissionSuccess = false;

    async function handleSubmit() {
        submissionError = null;
        submissionSuccess = false;

        try {
            const response = await patch(`/tasks/${taskId}/status`, { status: selectedStatus });
            if (response.message === 'Task status updated') {
                submissionSuccess = true;
            } else {
                submissionError = "Failed to update status";
            }
        } catch (error) {
            submissionError = error.message || "An unexpected error occurred.";
        }
    }
</script>

{#if submissionSuccess}
    <p style="color: green;">Status updated</p>
{/if}

<form on:submit|preventDefault={handleSubmit}>
    <label for="status">Status:</label>
    <select id="status" bind:value={selectedStatus}>
        <option value="not started">not started</option>
        <option value="in progress">in progress</option>
        <option value="completed">completed</option>
    </select>

    <button type="submit">Update Status</button>
</form>

{#if submissionError}
    <p style="color: red;">{submissionError}</p>
{/if}

<style>
    form {
        border: 1px solid #ccc;
        padding: 20px;
        border-radius: 5px;
        max-width: 400px;
        margin: 20px auto;
    }

    label {
        display: block;
        margin-bottom: 5px;
    }

    select {
        width: 100%;
        padding: 8px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    button {
        background-color: #4caf50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    button:hover {
        background-color: #45a049;
    }
</style>
