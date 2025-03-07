<script>
    import { post } from "../utils/api";
    import { get } from "../utils/api"; // Import get
    import { onMount } from 'svelte'; // Import onMount

    export let teams = [];
    export let allUsers = [];

    let selectedTeam = "";
    let selectedUsers = new Set();
    let selectedUsersToRemove = new Set(); // new
    let error = "";
    let success = "";
    let removeError = ""; // new
    let removeSuccess = ""; // new

    const handleUserChange = (userId) => {
        if (selectedUsers.has(userId)) {
            selectedUsers.delete(userId);
        } else {
            selectedUsers.add(userId);
        }
        selectedUsers = selectedUsers; // Trigger reactivity
    };

    // new function
    const handleUserRemoveChange = (userId) => {
        if (selectedUsersToRemove.has(userId)) {
            selectedUsersToRemove.delete(userId);
        } else {
            selectedUsersToRemove.add(userId);
        }
        selectedUsersToRemove = selectedUsersToRemove; // Trigger reactivity
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        error = "";
        success = "";

        if (!selectedTeam) {
            error = "Please select a team";
            return;
        }

        if (selectedUsers.size === 0) {
            error = "Please select at least one user";
            return;
        }

        try {
            const data = await post(`/teams/${selectedTeam}/users`, {
                user_ids: Array.from(selectedUsers),
            });
            if (data.message && data.message.startsWith("Added")) {
                success = data.message;
                selectedTeam = "";
                selectedUsers.clear();
                selectedUsers = selectedUsers; // Trigger reactivity
            } else {
                error = data.message || "Error adding users to team";
            }
        } catch (err) {
            console.error(err);
            error = "Error adding users to team";
        }
    };

    // new function
    const handleRemoveSubmit = async (event) => {
        event.preventDefault();
        removeError = "";
        removeSuccess = "";

        if (!selectedTeam) {
            removeError = "Please select a team";
            return;
        }

        if (selectedUsersToRemove.size === 0) {
            removeError = "Please select at least one user to remove";
            return;
        }

        try {
            // Use api.post for DELETE request
            const data = await post(`/teams/${selectedTeam}/users`, {
                user_ids: Array.from(selectedUsersToRemove),
                _method: 'DELETE' // Override method to DELETE
            });

            if (data.message === "Users removed successfully") {
                removeSuccess = "Users removed successfully";
                selectedUsersToRemove.clear();
                selectedUsersToRemove = selectedUsersToRemove; // Trigger reactivity
                // Refresh user list (assuming you have a function to fetch users)
                // await fetchUsers(); // You'll need to implement fetchUsers
                // A simpler approach is to reload the page
                window.location.reload();
            } else {
                removeError = data.message || "Error removing users from team";
            }
        } catch (err) {
            console.error(err);
            removeError = "Error removing users from team";
        }
    };

    // Function to fetch users (example - implement as needed)
    async function fetchUsers() {
        try {
            const users = await get('/users'); // Replace with your actual endpoint
            allUsers = users;
        } catch (error) {
            console.error("Error fetching users:", error);
            // Handle error as needed
        }
    }

    // Load users on component mount
    onMount(async () => {
        // await fetchUsers(); // Load users when the component is mounted
    });
</script>

<form id="team-users-form" on:submit={handleSubmit}>
    <div class="form-group">
        <label for="team-select">Team:</label>
        <select
            bind:value={selectedTeam}
            id="team-select"
            name="team"
            class="form-control"
        >
            <option value="">-- Select a Team --</option>
            {#each teams as team (team.id)}
                <option value={team.id}>{team.name}</option>
            {/each}
        </select>
    </div>

    <div class="form-group">
        <fieldset>
            <legend>Users:</legend>
            <div class="user-checkboxes">
                {#each allUsers as user (user.id)}
                    <label class="checkbox-label">
                        <input
                            type="checkbox"
                            name="users"
                            value={user.id}
                            class="user-checkbox"
                            on:change={() => handleUserChange(user.id)}
                            checked={selectedUsers.has(user.id)}
                        />
                        {user.username}
                    </label>
                {/each}
            </div>
        </fieldset>
    </div>

    <button type="submit" class="submit-btn"> Add Users </button>

    {#if success}
        <div class="success">{success}</div>
    {/if}
    {#if error}
        <div class="error">{error}</div>
    {/if}
</form>

<!-- new form -->
<form id="remove-users-form" on:submit={handleRemoveSubmit}>
    <div class="form-group">
        <fieldset>
            <legend>Remove Users:</legend>
            <div class="user-checkboxes">
                {#each allUsers as user (user.id)}
                    <label class="checkbox-label">
                        <input
                            type="checkbox"
                            name="removeUsers"
                            value={user.id}
                            class="user-checkbox"
                            on:change={() => handleUserRemoveChange(user.id)}
                            checked={selectedUsersToRemove.has(user.id)}
                        />
                        {user.username}
                    </label>
                {/each}
            </div>
        </fieldset>
    </div>

    <button type="submit" class="submit-btn"> Remove Users </button>

    {#if removeSuccess}
        <div class="success">{removeSuccess}</div>
    {/if}
    {#if removeError}
        <div class="error">{removeError}</div>
    {/if}
</form>

<style>
    .form-group {
        margin: 1rem 0;
    }

    .user-checkboxes {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }

    .checkbox-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .submit-btn {
        margin-top: 1rem;
    }

    .error {
        color: red;
    }
    .success {
        color: green;
    }
</style>
