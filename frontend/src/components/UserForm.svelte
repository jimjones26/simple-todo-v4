<script>
  import { createEventDispatcher } from "svelte";

  let username = "";
  let email = "";
  let password = "";
  let role = "";

  let usernameError = "";
  let emailError = "";
  let passwordError = "";
  let roleError = "";

  const dispatch = createEventDispatcher();

  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
  }

  function validateForm() {
    usernameError = username ? "" : "Username is required";
    emailError = email
      ? validateEmail(email)
        ? ""
        : "Invalid email format"
      : "Email is required";
    passwordError = password ? "" : "Password is required";
    roleError = role ? "" : "Role is required";

    return !usernameError && !emailError && !passwordError && !roleError;
  }

  function handleSubmit() {
    if (validateForm()) {
      const userData = { username, email, password, role };
      dispatch("submit", userData);
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="username">Username:</label>
    <input type="text" id="username" bind:value={username} />
    {#if usernameError}
      <p class="error">{usernameError}</p>
    {/if}
  </div>

  <div>
    <label for="email">Email:</label>
    <input type="email" id="email" bind:value={email} />
    {#if emailError}
      <p class="error">{emailError}</p>
    {/if}
  </div>

  <div>
    <label for="password">Password:</label>
    <input type="password" id="password" bind:value={password} />
    {#if passwordError}
      <p class="error">{passwordError}</p>
    {/if}
  </div>

  <div>
    <label for="role">Role:</label>
    <input type="text" id="role" bind:value={role} />
    {#if roleError}
      <p class="error">{roleError}</p>
    {/if}
  </div>

  <button type="submit">Create User</button>
</form>

<style>
  .error {
    color: red;
  }
</style>
