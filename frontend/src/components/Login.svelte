<script>
  let username = '';
  let password = '';
  let usernameError = '';
  let passwordError = '';

  function handleSubmit() {
    usernameError = username ? '' : 'Username is required';
    passwordError = password ? '' : 'Password is required';

    if (usernameError || passwordError) {
      return; // Prevent submission if there are errors
    }

    // In a real application, you would submit the form here
    // using the `fetch` API or a similar method.
    console.log('Form submitted', { username, password });
  }
</script>

<form on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="username">Username</label>
    <input type="text" id="username" bind:value={username} />
    {#if usernameError}
      <p class="error">Username is required</p>
    {/if}
  </div>

  <div>
    <label for="password">Password</label>
    <input type="password" id="password" bind:value={password} />
    {#if passwordError}
      <p class="error">Password is required</p>
    {/if}
  </div>

  <button type="submit">Login</button>
</form>

<style>
  .error {
    color: red;
  }
</style>
