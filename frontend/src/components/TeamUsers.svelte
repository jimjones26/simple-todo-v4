<script>
    import { post } from "../utils/api";

    export let teams = [];
    export let allUsers = [];

    let selectedTeam = "";
    let selectedUsers = new Set();
    let error = "";
    let success = "";

    const handleUserChange = (userId) => {
        if (selectedUsers.has(userId)) {
            selectedUsers.delete(userId);
        } else {
            selectedUsers.add(userId);
        }
        selectedUsers = selectedUsers; // Trigger reactivity
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
