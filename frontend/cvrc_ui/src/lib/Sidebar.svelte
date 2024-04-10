<!--Main Navigation-->
<script>
    import { createEventDispatcher } from 'svelte';
    let dispatch = createEventDispatcher();
    
    export let components;
    export let activeComponent;
</script>

<header>
    <!-- Sidebar -->
    <nav id="sidebarMenu" class="collapse d-lg-block sidebar bg-white">
        <div class="position-sticky">
            <div class="list-group list-group-flush mx-3 mt-4">
                <p class="list-group-item list-group-item-action py-2 ripple" aria-current="true">
                    <i class="fas fa-tachometer-alt fa-fw me-3"></i><span>Main dashboard</span>
                </p>
    
                {#each components as component}
                <div class="{activeComponent === component ? 'active' : ''}" style="margin:0;padding:0;">
                    <p class="list-group-item list-group-item-action py-2 ripple" on:click={() => dispatch('tabChange',component)}>
                        <i class="fas fa-chart-area fa-fw me-3"></i><span>{component}</span>
                    </p>
                </div>
                {/each}
            </div>
        </div>
    </nav>
    <!-- End Sidebar -->
</header>

<style>
    @media (min-width: 991.98px) {
        main {
            padding-left: 240px;
        }
    }


    /* Sidebar */
    .sidebar {
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        padding-top: 58px; /* Height of navbar */
        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.05), 0 2px 10px 0 rgba(0, 0, 0, 0.05);
        width: 240px;
        z-index: 600;
        overflow-y: auto;
    }

    @media (max-width: 991.98px) {
        .sidebar {
            width: 100%;
        }
    }
  .active .list-group-item {
        background-color: green;
        color: white;
           padding:0;
        margin:0;
        cursor: pointer;
        margin-bottom: 0.5rem; 
        border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
        
    }
    .sidebar .active {
        border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
    }

    .position-sticky {
        height: calc(100vh - 58px); /* Adjust for navbar height */
        overflow-y: auto; /* Scrollable contents */
    }

    .list-group-item {
        padding:0;
        margin:0;
        cursor: pointer;
        margin-bottom: 0.5rem; 
        border-radius: 5px;
        box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
    }
</style>
