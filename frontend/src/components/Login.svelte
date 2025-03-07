<script>
  import { post } from "../utils/api";
  import { auth } from "../stores/authStore";

  let username = "";
  let password = "";
  let usernameError = "";
  let passwordError = "";
  let error = "";

  async function handleSubmit() {
    usernameError = username ? "" : "Username is required";
    passwordError = password ? "" : "Password is required";

    if (usernameError || passwordError) {
      return;
    }

    error = "";
    try {
      const response = await post("/login", { username, password });
      if (!response.ok) {
        const data = await response.json();
        error = data.message || "Invalid credentials";
      } else {
        const user = await response.json();
        auth.set({ isAuthenticated: true, user, isLoading: false });
      }
    } catch (err) {
      console.error("Login failed:", err);
      error = "Network error or invalid response";
    }
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="username">Username:</label>
    <input id="username" type="text" bind:value={username} />
    {#if usernameError}
      <p class="error">{usernameError}</p>
    {/if}
  </div>
  <div>
    <label for="password">Password:</label>
    <input id="password" type="password" bind:value={password} />
    {#if passwordError}
      <p class="error">{passwordError}</p>
    {/if}
  </div>
  <button type="submit">Login</button>
  {#if error}
    <p class="error">{error}</p>
  {/if}
</form>

<style>
  .error {
    color: red;
  }
</style>
