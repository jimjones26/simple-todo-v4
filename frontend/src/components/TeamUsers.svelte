<script>
    export let teams = []; // Array of team objects {id, name}
    export let allUsers = []; // Array of user objects {id, username}
</script>

<form id="team-users-form">
    <div class="form-group">
        <label for="team-select">Team:</label>
        <select id="team-select" name="team" class="form-control">
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
                        />
                        {user.username}
                    </label>
                {/each}
            </div>
        </fieldset>
    </div>

    <button type="submit" class="submit-btn"> Add Users </button>
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
</style>
