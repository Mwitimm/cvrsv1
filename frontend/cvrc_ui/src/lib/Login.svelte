<script>
  import { goto } from '$app/navigation';
  import login from "$lib/login.js"
  import Loading from "$lib/Loading.svelte"
  
  import toast, { Toaster } from 'svelte-french-toast';




  let email = '';
  let password = '';
  let isLoading = false;




  function handleSubmit() {
    isLoading = true;

    const data = {
      email: email,
      password: password
    };

    

    fetch('http://localhost:8080/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Login failed');
      }
      return response.json();
    })
    .then(data => {

      console.log('Login successful:', data);
      login.set({ isLoggedIn: true, userInfo: data });
      isLoading = false;

      toast.success("Login successful");
      setTimeout(() => {
  
        goto("/");
      }, 1000);
     
    
    })
    .catch(error => {
      console.error('There was a problem with the login:', error);
      isLoading = false;
      toast.error("Check your password or email and try again",
      {
        duration:4000
      }
      
      )
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
    background:none;
      color: #333;
      font-size: 16px;
      outline: none;
      transition: border-color 0.3s ease;
    }
  
    .agricultural-theme .form-control:focus {
      border-color: #689f38;
    }
  
    /* Remove input highlight on select */
    .agricultural-theme .form-control::selection {
      background-color: transparent;
    }
  
    /* Remove blue outline on focus */
    .agricultural-theme input:focus {
      outline: none;
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
  
    /* Signup section styles */
    .signup {
      text-align: center;
      margin-top: 30px;
    }
  
    .signup p {
      color: #4caf50;
      font-size: 16px;
      margin-bottom: 10px;
    }
  
    .signup a {
      color: #689f38;
      text-decoration: none;
      font-weight: bold;
      transition: color 0.3s ease;
    }
  
    .signup a:hover {
      color: #558b2f;
    }

    
</style>





<div class="container agricultural-theme">
  <h2>Login</h2>
  <!-- Add a conditional rendering for the loader -->
  {#if isLoading}
  <Loading/>
  {:else}
    <form on:submit|preventDefault={handleSubmit}>
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

      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  {/if}
   <div class="signup">
    <p>Don't have an account?</p>
    <a href="/signup">Sign Up</a>
  </div>
<Toaster/>
</div>


