<script>
    import { onMount } from 'svelte';
    import login from "$lib/login.js"

    let userInfo;
    let loginState
    const unsubscribe = login.subscribe(value => {
        userInfo = value.userInfo;
        loginState = value.isLoggedIn
        console.log("state",loginState,"User info:", userInfo);
    });


    function logout() {
        login.set({ isLoggedIn: false, userInfo: null });
    }
    // Unsubscribe when the component is destroyed to avoid memory leaks
    onMount(() => {
        return () => {
            unsubscribe();
        };
    });


</script>

<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Agritech</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-center" id="navbarSupportedContent">
            <ul class="navbar-nav mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/">About Us</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/">Services</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="/">Dashboard</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/values">Crops</a>
                </li>
            </ul>
        </div>
        <ul class="navbar-nav">
        {#if userInfo && loginState}
        <li class="nav-item dropdown" ms-auto>
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                <img src="images/profile.jpg" alt="Profile" width="20" height="20" class="me-1">
                {userInfo.username}
            </a>
            <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <li><a class="dropdown-item" href="#">Profile</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><button class="dropdown-item" on:click={logout}>Logout</button></li>
            </ul>
        </li>
            {:else}
                <li class="nav-item">
                    <a class="nav-link" href="/login">
                        <img src="images/profile.jpg" alt="Login" width="20" height="20" class="me-1">Login
                    </a>
                </li>
            {/if}
        </ul>
    </div>
</nav>


<style>
    nav{
        position:fixed;
        width: 100%;
    }
</style>