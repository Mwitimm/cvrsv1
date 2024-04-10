<script>
    import { onMount } from 'svelte';
    import specific from "$lib/specific.js";
    import prediction from "$lib/Store.js";
  
    let predictedCrop = '';
    let specificVarieties = [];
  
    onMount(() => {
      prediction.subscribe(value => {
        predictedCrop = value;
      });

    
  
      specific.subscribe(crops => {
        specificVarieties = Array.from(crops).sort((a, b) => {
          const attributesA = a.specialattributes ? a.specialattributes.split(',').length : 0;
          const attributesB = b.specialattributes ? b.specialattributes.split(',').length : 0;
          return attributesB - attributesA;
        });
      });
    });

    function handleFeedbackClick(variety) {
      // console.log(`Feedback button clicked for variety: ${variety.cropname}`);
      alert("cliked")
     }

     function Feedback(variety){
       console.log("The seleted variety",variety)
     }
  
    function handleNull(value) {
      return value === null ? 'N/A' : value;
    }
  </script>
  
  {#if specificVarieties.length > 0}
    {#each specificVarieties.slice(0, 3) as variety, index}
      <div class="card" class:index={index === 0 ? 'highlighted' : ''}>
        <h2>{variety.cropname}</h2>
        <p>Variety: {handleNull(variety.varietyname)}</p>
        <p>Duration to Maturity (Months): {handleNull(variety.durationtomaturitymonths)}</p>
        <p>Economic Production Life (Years): {handleNull(variety.economicproductionlifeyears)}</p>
        <p>Maintainer Seedling Source: {handleNull(variety.maintainerseedlingsource)}</p>
        <p>Optimal Production Altitude: {handleNull(variety.optimalproductionaltitude)}</p>
        <p>Special Attributes: {handleNull(variety.specialattributes)}</p>
        <p>Year of Release: {handleNull(variety.yearofrelease)}</p>
        <p>Yield per Tree per Year: {handleNull(variety.yieldpertreeperyear)}</p>
        <button on:click={() => Feedback(variety)}>
        Give Feedback
      </button>
      </div>
    {/each}
  {:else}
    <h2>No data available for {predictedCrop}</h2>
  {/if}
  
  <style>
    .card {
    border: 1px solid #8b4513; /* Rustic brown color */
    border-radius: 5px;
    padding: 20px;
    margin-top:auto;
    margin-bottom:20px;
    background-color: #f5f5dc; /* Beige color */
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  }

  .highlighted {
    background-color: #7cfc00; /* Lime green color */
  }

  h2 {
    /*font-family: 'Brush Script MT', cursive;*/
    padding-top:25px;
    margin-top:10px;
    color: #008000; /* Dark green color */
    text-align: center;
  }

  p {
    font-family: 'Georgia', serif;
    color: #2f4f4f; /* Dark slate gray color */
  }
  </style>
  