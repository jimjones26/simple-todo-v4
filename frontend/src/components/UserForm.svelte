<script>
  import { post } from '../utils/api';

  let username = "";
  let email = "";
  let password = "";
  let role = "";

  let usernameError = "";
  let emailError = "";
  let passwordError = "";
  let roleError = "";
  let submissionError = "";
  let submissionSuccess = false;

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

  async function handleSubmit(event) {
    event.preventDefault(); // Prevent default form submission
    submissionError = ""; // Clear any previous submission errors
    submissionSuccess = false;

    if (validateForm()) {
      const userData = { username, email, password, role };

      try {
        const response = await post('/users', userData);
        // Handle successful submission
        submissionSuccess = true;
        // Clear the form
        username = "";
        email = "";
        password = "";
        role = "";
      } catch (error) {
        // Handle submission errors
        submissionError = error.message || "An unexpected error occurred.";
      }
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  {#if submissionSuccess}
    <p class="success">User created successfully!</p>
  {/if}

  {#if submissionError}
    <p class="error">{submissionError}</p>
  {/if}

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
  .success {
    color: green;
  }
</style>
