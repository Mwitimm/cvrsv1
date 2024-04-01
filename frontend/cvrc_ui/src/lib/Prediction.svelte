<script>
  import { onMount } from 'svelte';
  import prediction from '$lib/Store.js';
  import varieties from "$lib/varieties.js"
  import { goto } from '$app/navigation';

  let formData = {
    N: '',
    P: '',
    K: '',
    temperature: '',
    humidity: '',
    ph: '',
    rainfall: '',
  };

  // Load form data from localStorage on component mount
  onMount(() => {
    const storedFormData = localStorage.getItem('formData');
    if (storedFormData) {
      formData = JSON.parse(storedFormData);
    }
  });

  let results = '';

  let isLoading = false;

 /* async function predictCrop() {
    isLoading = true;
    const response = await fetch('http://localhost:8080/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });

    const data = await response.json();
    prediction.set(data.prediction);
    prediction.subscribe((value) => {
      results = value;
      console.log(results);
    });
    console.log(results);

    //const varietiesResponse = await fetch(`http://localhost:8080/varieties?cropname=${value}`);
    const varietiesResponse = await fetch(`http://localhost:8080/varieties?cropname=${value}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const varietiesData = await varietiesResponse.json();
    varieties.set(varietiesData);  

    // Save form data to localStorage

    localStorage.setItem('formData', JSON.stringify(formData));
    isLoading = false;

    // Navigate to the results page
    goto('/results');
  }  */ 

  
async function predictCrop() {
  isLoading = true;

  const response = await fetch('http://localhost:8080/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(formData),
  });

  const data = await response.json();
  const value = data.prediction;
  prediction.set(value);
  results = value;
  console.log(results);

  const varietiesResponse = await fetch(`http://localhost:8080/varieties?cropname=${value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  });

  const varietiesData = await varietiesResponse.json();
  varieties.set(varietiesData);

  // Save form data to localStorage
  //localStorage.setItem('formData', JSON.stringify(formData));

  isLoading = false;

  // Navigate to the results page
  goto('/results');
}

  function handleInputChange(event) {
    const { name, value } = event.target;
    formData[name] = value;
  }
</script>





<main>

  <form on:submit|preventDefault={predictCrop} class="centered-form">
    <div class="form-container">

        {#if isLoading}
      <div class="spinner"></div>
      {:else}
        <h1>Find the right crop</h1>
          <div class="form-group">
        <label for="N">Nitrogen</label>
        <input
          type="float"
          id="N"
          name="N"
          bind:value={formData.N}
          on:input={handleInputChange}
          placeholder="eg 90.01"
          required
        />
      </div>

      <div class="form-group">
        <label for="P">Phosphorus</label>
        <input
          type="float"
          id="P"
          name="P"
          bind:value={formData.P}
          on:input={handleInputChange}
          placeholder="eg 42.07"
          required
        />
      </div>

      <div class="form-group">
        <label for="K">Potassium</label>
        <input
          type="float"
          id="K"
          name="K"
          bind:value={formData.K}
          on:input={handleInputChange}
          placeholder="eg 43.00"
          required
        />
      </div>

      <div class="form-group">
        <label for="temperature">Temperature: (°C)</label>
        <input
          type="float"
          id="temperature"
          name="temperature"
          bind:value={formData.temperature}
          on:input={handleInputChange}
          placeholder="eg 20.877"
          required
        />
      </div>

      <div class="form-group">
        <label for="humidity">Humidity:</label>
        <input
          type="float"
          id="humidity"
          name="humidity"
          bind:value={formData.humidity}
          on:input={handleInputChange}
          placeholder="eg 82.00"
          required
        />
      </div>

      <div class="form-group">
        <label for="ph">Acidity Level</label>
        <input
          type="float"
          id="ph"
          name="ph"
          bind:value={formData.ph}
          on:input={handleInputChange}
          placeholder="eg 6.5"
          required
        />
      </div>

      <div class="form-group">
        <label for="rainfall">Rainfall (mm)</label>
        <input
          type="float"
          id="rainfall"
          name="rainfall"
          bind:value={formData.rainfall}
          on:input={handleInputChange}
          placeholder="202.9355"
          required
        />
      </div>

      <div>
        <button type="submit" class="button">Next</button>
      </div>

    
    {/if}

  
    </div>
    
  </form>
</main>



<style>
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
    display: flex;
    justify-content: center;
    align-items: center;
    height: auto;
  }

  .form-container {
    width: 75vh;
    border: 1px solid #ccc;
    border-radius: 5px;
    background-color: #fff;
    padding: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }

  .centered-form {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }

  .form-container h1 {
    color: rgba(0, 128, 0, 10);
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
  }

  .form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
  }

  .button {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: rgba(0, 128, 0, 10);
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  a {
    text-decoration: none;
  }

  button:hover {
    background-color: #555;
  }

  p {
    margin-top: 20px;
  }

  .spinner {
    border: 5px solid rgba(0, 0, 0, 0.1);
    border-left-color: rgba(0, 0, 0, 0.5);
    border-radius: 50%;
    width: 500px;
    height: 500px;
    animation: spin 1s linear infinite;
    margin: 0 auto;
  position: fixed;
  

	background: url('images/yin-yen.gif')center ;
  
  }

  /*@keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }*/
</style>