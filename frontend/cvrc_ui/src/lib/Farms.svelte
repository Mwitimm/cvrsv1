<script>
  import { onMount } from 'svelte';
  import login from "$lib/login.js"
  import toast, { Toaster } from 'svelte-french-toast';

  let userInfo;
  let loginState;
  const unsubscribe = login.subscribe(value => {
      userInfo = value.userInfo;
      loginState = value.isLoggedIn;
      console.log("state", loginState, "User info:", userInfo);
  });

  // Unsubscribe when the component is destroyed to avoid memory leaks
  onMount(async () => {
    await fetchData();
  
    return () => {
      unsubscribe();
    };
  });

  let farm = {
      user_id: userInfo.user_id,
      farm_name: '',
      location: '',
      size: 0,
      soil_type: '',
      climate_zone: ''
  };

  async function addFarm() {

      try {
          const response = await fetch('http://localhost:8080/farm', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify(farm)
          });

          if (response.ok) {
            await fetchData();
             toast.success("Farm added successfuly");
             farm = {
              user_id: userInfo.user_id,
              farm_name: '',
              location: '',
              size: 0,
              soil_type: '',
              climate_zone: ''
          };
          } else {
            toast.error("Failed to add farm try again later",
            {
              duration:4000
            }
            
            )
          }
      } catch (error) {
          console.error('Error adding farm:', error);
          alert('Failed to add farm.');
      }
  }

  let Farms = [];

  async function fetchData() {
    try {
      const response = await fetch(`http://localhost:8080/farms/${userInfo.user_id}`);
      if (response.ok) {
        const data = await response.json();
        Farms = data.farms;
        console.log(Farms);
      } else {
        console.error('Failed to fetch farm data');
      }
    } catch (error) {
      console.error('Error fetching farm data:', error);
    }
  }

  async function deleteFarm(farmId) {
    try {
        const response = await fetch(`http://localhost:8080/deletefarm/${farmId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            // Farm deleted successfully
            await fetchData();
            toast.success("Farm Deleted")
            await fetchData();
            


            // You may want to update UI or perform other actions after deletion
        } else {
            // Failed to delete farm
             toast.error("Failed to delete")
             await fetchData();
            // You can handle the error or display a message to the user
        }
    } catch (error) {
        // Error occurred during deletion process
        console.error('Error deleting farm:', error);
        // You can handle the error or display a message to the user
    }
}


  

</script>
<Toaster/>
<div class="container">
  <div class="row">
    <div class="col-md-6">
      <h1 class="mb-4">Farm Data</h1>
        <table class="table table-striped">
          <thead>
            <tr>
              <th>Farm Name</th>
              <th>Location</th>
              <th>Size (Acres)</th>
              <th>Soil Type</th>
              <th>Climate Zone</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {#if Farms.length > 0}
              {#each Farms as farm}
                <tr>
                  <td>{farm.farm_name}</td>
                  <td>{farm.location}</td>
                  <td>{farm.size}</td>
                  <td>{farm.soil_type}</td>
                  <td>{farm.climate_zone}</td>
                  <td>
                    <button class="btn btn-danger" on:click={async () => await deleteFarm(farm.farm_id)}>Delete</button>
                  </td>
                </tr>
              {/each}
            {:else}
              <tr>
                <td colspan="6">You have not added any farms yet.</td>
              </tr>
            {/if}
          </tbody>
        
           
    </div>

    <div class="col-md-6">
      <h1 class="mb-4">Add Farm</h1>
      <form class="row g-3" on:submit={addFarm}>
        <div class="col-md-12">
          <div class="mb-3">
            <label for="farmName" class="form-label">Farm Name</label>
            <input type="text" class="form-control" id="farmName" placeholder="Enter farm name" bind:value={farm.farm_name}>
          </div>
          <div class="mb-3">
            <label for="location" class="form-label">Location</label>
            <input type="text" class="form-control" id="location" placeholder="Enter location" bind:value={farm.location}>
          </div>
          <div class="mb-3">
            <label for="size" class="form-label">Size (Acres)</label>
            <input type="number" class="form-control" id="size" placeholder="Enter size" bind:value={farm.size}>
          </div>
          <div class="mb-3">
            <label for="soilType" class="form-label">Soil Type</label>
            <input type="text" class="form-control" id="soilType" placeholder="Enter soil type" bind:value={farm.soil_type}>
          </div>
          <div class="mb-3">
            <label for="climateZone" class="form-label">Climate Zone</label>
            <input type="text" class="form-control" id="climateZone" placeholder="Enter climate zone" bind:value={farm.climate_zone}>
          </div>
        </div>
        <div class="col-md-12">
          <button type="submit" class="btn btn-primary">Add</button>
        </div>
      </form>
    </div>
  </div>
</div>


