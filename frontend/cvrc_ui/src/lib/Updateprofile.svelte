


<script>
    import { onMount } from 'svelte';
       import login from "$lib/login.js"

       import toast, { Toaster } from 'svelte-french-toast';
  
    let user = {

      phone_number: '',
      language: '',
      
    };
 



    let userInfo;
    let loginState
    const unsubscribe = login.subscribe(value => {
        userInfo = value.userInfo;
        loginState = value.isLoggedIn
        console.log("state",loginState,"User info:", userInfo);
    });

    




    async function fetchUserData() {
        try {
            const response = await fetch(`http://localhost:8080/user/${userInfo.user_id}`); // Assuming user_id is available in userInfo
            if (response.ok) {
                const userData = await response.json();
                // Populate user object with fetched data
                userInfo = {
                    ...userInfo,
                    ...userData
                };
            console.log(userInfo)
            } else {
                console.error('Failed to fetch user data');
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
        }
    }

    onMount(() => {
        fetchUserData();
    });

    async function updateProfile() {
        try {
            // Send updated user data to the server
            const response = await fetch(`http://localhost:8080/updateuser/${userInfo.user_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(user)
            });
    
            if (response.ok) {
                // Handle successful update
                
                user = {

                  phone_number: '',
                  language: '',
                  
                };
                toast.success("Profile updated sucessfully")
                fetchUserData()
            } else {
                // Handle error
                 toast.error("Failed to update profile")
            }
        } catch (error) {
            console.error('Error updating profile:', error);
            alert('Failed to update profile.');
        }
    }
    
  </script>


  <Toaster/>
  
  <div class="container">
    <h1 class="mb-4">Update Profile</h1>
  
    <div class="row">
      <div class="col-md-6">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input type="text" class="form-control" id="username" bind:value={userInfo.username} disabled>
        </div>
  
        <div class="mb-3">
          <label for="firstName" class="form-label">First Name</label>
          <input type="text" class="form-control" id="firstName" bind:value={userInfo.first_name} disabled>
        </div>
  
        <div class="mb-3">
          <label for="lastName" class="form-label">Last Name</label>
          <input type="text" class="form-control" id="lastName"  bind:value={userInfo.last_name} disabled>
        </div>
  
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input type="email" class="form-control" id="email"  bind:value={userInfo.email} disabled>
        </div>
  
        <div class="mb-3">
          <label for="phoneNumber" class="form-label">Phone Number</label>
          <input type="text" class="form-control" id="phoneNumber" bind:value={user.phone_number}  required>
        </div>
  
        <div class="mb-3">
          <label for="language" class="form-label">Language</label>
          <input type="text" class="form-control" id="language" bind:value={user.language}  required>
        </div>
      </div>

    </div>
  
    <button class="btn btn-primary" on:click={updateProfile}>Update Profile</button>
  </div>