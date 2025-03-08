<script>
    let selectedStatus = "not started"; // Default status

    function handleSubmit() {
        // Implementation for form submission will go here in a later step
        console.log("Selected status:", selectedStatus); // Placeholder action
    }
</script>

<form on:submit|preventDefault={handleSubmit}>
    <label for="status">Status:</label>
    <select id="status" bind:value={selectedStatus}>
        <option value="not started">not started</option>
        <option value="in progress">in progress</option>
        <option value="completed">completed</option>
    </select>

    <button type="submit">Update Status</button>
</form>

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
