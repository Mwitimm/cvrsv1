<script>
  import { onMount } from 'svelte';
  import prediction from "$lib/Store.js";
  import varieties from "$lib/varieties.js"
  import specific from "$lib/specific.js"
  import { goto } from '$app/navigation';
  
  import Test from "$lib/Test.svelte";

  let formData = {
    altitude: "",
    Months: ""
  };

  let months = [];
  let altitudes=[]

  let predictedCrop = '';
  let compactibility = ''
  let returnedVarieties
  let uniqueMonths = [];
  let uniqueAltitudes = [];
  let isLoading = false;

  onMount(() => {
    prediction.subscribe(value => {
      predictedCrop = value.prediction; 
      compactibility = value.compactibility
      console.log(predictedCrop,"score is", compactibility);
    });

   varieties.subscribe(crops => {
      returnedVarieties = crops; 
      console.log(returnedVarieties);
    });

    months = getUniqueMonths();
    altitudes = getUniqueAltitudes();





  
  

  });




console.log(months)

  function handleInputChange(event) {
    const { name, value } = event.target;
    formData[name] = value;
  }

  function getUniqueMonths() {
    if (!returnedVarieties[predictedCrop] || returnedVarieties[predictedCrop].length === 0) {
      return [];
    }
  
    const uniqueMonths = new Set();
  
    returnedVarieties[predictedCrop].forEach(variety => {
      if (variety.durationtomaturitymonths !== null) {
        uniqueMonths.add(variety.durationtomaturitymonths);
      }
    });
  
    console.log(uniqueMonths);
    return Array.from(uniqueMonths).sort((a, b) => a - b);
  }
  
  function getUniqueAltitudes() {
    if (!returnedVarieties[predictedCrop] || returnedVarieties[predictedCrop].length === 0) {
      return [];
    }
  
    const uniqueAltitudes = new Set();
  
    returnedVarieties[predictedCrop].forEach(variety => {
      if (variety.optimalproductionaltitude !== null) {
        uniqueAltitudes.add(variety.optimalproductionaltitude);
      }
    });
  
    console.log(uniqueAltitudes);
    return Array.from(uniqueAltitudes).sort((a, b) => a - b);
  }

  async function predictCrop() {
    const specificVarieties = await fetch(`http://localhost:8080/varieties/specific?altitude_range=${formData.altitude}&maturity_duration=${formData.Months}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    const specificData = await specificVarieties.json();
    specific.set(specificData)
    console.log(specificData)
    goto("/dashboard")
  }
</script>

<div class="container">
  <h1 class="title">Crop reccommendation</h1>
  
  {#if predictedCrop}
    <div class="prediction-section">
      <p class="prediction-text">We have reccommended:</p>
      <p class="prediction-result">{predictedCrop}</p>
      <p class="prediction-text">
           compactibility
      </p>
      <small class="prediction-result">{compactibility}</small>
    </div>
  {:else if isLoading}
    <div class="prediction-section">
      <p class="prediction-text">Loading...</p>
    </div>
  {/if}
  
  <form class="centered-form" on:submit|preventDefault={predictCrop}>
    <div class="form-container">
      <h2 class="form-title">Fill in the form below</h2>

        <div class="form-group">
        <label for="altitude">Altitude</label>
        <select id="altitude" name="altitude" bind:value={formData.altitude} on:change={handleInputChange}>
          <option value="">Select Altitude</option>
          {#each altitudes as altitude}
            <option value={altitude}>{altitude}</option>
          {/each}
        </select>
      </div>

         <div class="form-group">
        <label for="months">Duration to Maturity (Months)</label>
        <select id="months" name="months" bind:value={formData.Months} on:change={handleInputChange}>
       <option value="">Select a month</option>
    {#each months as month}
      <option value={month}>{month} months</option>
    {/each}
        </select>
      </div>
  
    
  
  
      <div>
        <button type="submit" class="button">Predict</button>
      </div>
    </div>
  </form>
</div>

<style>
  /*
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f4f4f4;
  }

  .container {
    max-width: 800px;
    margin: 20px auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .title {
    color: rgba(0, 128, 0, 10);
    text-align: center;
    margin-bottom: 20px;
  }

  .prediction-section {
    margin-bottom: 20px;
    padding: 10px;
    border-radius: 5px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .prediction-text {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }

  .prediction-result {
    font-size: 16px;
    color: #666;
  }

  .centered-form {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
  }

  .form-container {
    width: 100%;
    max-width: 400px;
  }

  .form-title {
    color: rgba(0, 128, 0, 10);
    text-align: center;
    margin-bottom: 20px;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    color: #333;
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
 
  .button:hover {
    background-color: #008000;
  }*/


    body {
    font-family: 'Roboto', sans-serif;
    margin: 0;
    padding: 0;
    background-color: #f8f8e6;
  }

  .container {
    max-width: 800px;
    margin: 40px auto;
    padding: 40px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    position: relative;
  }

  .container::before {
    content: "";
    background-image: url('https://source.unsplash.com/random/800x600/?agriculture');
    background-size: cover;
    background-position: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    opacity: 0.1;
    z-index: -1;
  }

  .title {
    color: #4d7c0f;
    text-align: center;
    margin-bottom: 30px;
    font-size: 32px;
    font-weight: bold;
  }

  .prediction-section {
    margin-bottom: 30px;
    padding: 20px;
    border-radius: 8px;
    background-color: #f9f9f9;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    text-align: center;
  }

  .prediction-text {
    font-size: 20px;
    font-weight: bold;
    color: #333;
    margin-bottom: 10px;
  }

  .prediction-result {
    font-size: 18px;
    color: #4d7c0f;
    font-weight: bold;
  }

  .centered-form {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 30px;
  }

  .form-container {
    width: 100%;
    max-width: 400px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .form-title {
    color: #4d7c0f;
    text-align: center;
    margin-bottom: 20px;
    font-size: 24px;
    font-weight: bold;
  }

  .form-group {
    margin-bottom: 20px;
  }

  .form-group label {
    display: block;
    margin-bottom: 8px;
    color: #333;
    font-weight: bold;
  }

  .form-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
    font-size: 16px;
  }

  .button {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 4px;
    background-color: #4d7c0f;
    color: #fff;
    cursor: pointer;
    transition: background-color 0.3s;
    font-size: 16px;
    font-weight: bold;
  }

  .button:hover {
    background-color: #3a5e0c;
  }
</style>
