<script>
  import { goto } from '$app/navigation';
  import toast, { Toaster } from 'svelte-french-toast';

  import Loading from "$lib/Loading.svelte"

  let firstName = '';
  let lastName = '';
  let username = '';
  let email = '';
  let password = '';
  let passwordc = '';


  let isLoading = false; // Add a loading state

  function handleSubmit() {
    if (password !== passwordc) {
      alert('Passwords do not match');
      return;
    }
    
    // Set isLoading to true when the request starts
    isLoading = true;

    // Prepare data object to send
    const data = {
      username: username,
      password: password,
      first_name: firstName,
      last_name: lastName,
      email: email
    };

    // Make POST request to API
    fetch('http://localhost:8080/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      console.log('Signup successful');
  toast.success(
	"Account creation successful\nLogin to continue.",
	{
		duration: 2000,
	}
);
      goto("/login");
    })
    .catch(error => {
      
      console.error('There was a problem with the signup request:', error);
      toast.error(" There was a problem with the signup request \n Check your username or email and try again",
      {
        duration:4000
      }
      
      )
    
    })
    .finally(() => {
      // Set isLoading to false when the request completes (whether success or failure)
      isLoading = false;
    });
  }
  
  </script>
  
  <style>
    /* Agricultural project styling */
    .agricultural-theme {
      max-width: 500px;
      margin: 0 auto;
      padding: 40px;
      border-radius: 10px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      background-color: #fff;
    }
  
    .agricultural-theme h2 {
      color: #2e7d32;
      font-family: 'Georgia', serif;
      text-align: center;
      margin-bottom: 30px;
    }
  
    .agricultural-theme .form-group {
      margin-bottom: 20px;
    }
  
    .agricultural-theme .form-group label {
      color: #4caf50;
      font-weight: bold;
      display: block;
      margin-bottom: 5px;
    }
  
    .agricultural-theme .form-control {
      width: 100%;
      padding: 10px;
      border: none;
      border-bottom: 2px solid #8bc34a;
      background: none;
      background-color: transparent;
      color: #333;
      font-size: 16px;
      outline: none;
      transition: border-color 0.3s ease;
    }
  
    .agricultural-theme input {
      border: 0.5rem solid red;
    }
  
    .agricultural-theme .form-control:focus {
      border-color: #689f38;
    }
  
    /* Remove input highlight on select */
    .agricultural-theme .form-control::selection {
      background-color: transparent;
    }
  
    .agricultural-theme .btn-primary {
      background-color: #689f38;
      border-color: #689f38;
      color: #fff;
      padding: 10px 20px;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s ease;
      display: block;
      margin: 0 auto;
    }
  
    .agricultural-theme .btn-primary:hover {
      background-color: #558b2f;
      border-color: #558b2f;
    }
  
    /* Login section styles */
    .login {
      text-align: center;
      margin-top: 30px;
    }
  
    .login h1 {
      color: #689f38;
      font-family: 'Georgia', serif;
      font-size: 24px;
      margin-bottom: 10px;
    }
  
    .login p {
      color: #4caf50;
      font-size: 16px;
      margin-bottom: 10px;
    }
  
    .login a {
      color: #689f38;
      text-decoration: none;
      font-weight: bold;
      transition: color 0.3s ease;
    }
  
    .login a:hover {
      color: #558b2f;
    }

    .loader-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100%;
    }
  
    .loader {
      width: 40px;
      height: 20px;
      --c: no-repeat radial-gradient(farthest-side, #000 93%, #0000);
      background: var(--c) 0 0, var(--c) 50% 0, var(--c) 100% 0;
      background-size: 8px 8px;
      position: relative;
      animation: l4-0 1s linear infinite alternate;
    }
  
    .loader:before {
      content: "";
      position: absolute;
      width: 8px;
      height: 12px;
      background: #000;
      left: 0;
      top: 0;
      animation: l4-1 1s linear infinite alternate, l4-2 0.5s cubic-bezier(0, 200, .8, 200) infinite;
    }
  
    @keyframes l4-0 {
      0% {
        background-position: 0 100%, 50% 0, 100% 0;
      }
  
      8%, 42% {
        background-position: 0 0, 50% 0, 100% 0;
      }
  
      50% {
        background-position: 0 0, 50% 100%, 100% 0;
      }
  
      58%, 92% {
        background-position: 0 0, 50% 0, 100% 0;
      }
  
      100% {
        background-position: 0 0, 50% 0, 100% 100%;
      }
    }
  
    @keyframes l4-1 {
      100% {
        left: calc(100% - 8px);
      }
    }
  
    @keyframes l4-2 {
      100% {
        top: -0.1px;
      }
    }

  </style>
  
  <div class="container agricultural-theme">


    <h2>Signup</h2>

  {#if isLoading}

 <Loading/>
  
  {:else}
  <form on:submit|preventDefault={handleSubmit}>
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input
          type="text"
          class="form-control"
          id="firstName"
          bind:value={firstName}
          required
          autocomplete="off"
        />
      </div>
  
      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input
          type="text"
          class="form-control"
          id="lastName"
          bind:value={lastName}
          required
          autocomplete="off"
        />
      </div>
  
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="text"
          class="form-control"
          id="username"
          bind:value={username}
          required
          autocomplete="off"
        />
      </div>
  
      <div class="form-group">
        <label for="email">Email</label>
        <input
          type="email"
          class="form-control"
          id="email"
          bind:value={email}
          required
          autocomplete="off"
        />
      </div>
  
      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          class="form-control"
          id="password"
          bind:value={password}
          required
          autocomplete="off"
        />
      </div>
  
      <div class="form-group">
        <label for="password">Confirm Password</label>
        <input
          type="password"
          class="form-control"
          id="passwordc"
          bind:value={passwordc}
          required
          autocomplete="off"
        />
      </div>
  
      <button type="submit" class="btn btn-primary">Sign Up</button>
    </form>
  

  {/if}

    <div class="login">
      <h1>Or</h1>
      <p>Already have an account?</p>
      <a href="/login">Login</a>
    </div>

<Toaster />
    
  </div>