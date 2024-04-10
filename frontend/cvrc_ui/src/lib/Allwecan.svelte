<script>
    import { onMount } from 'svelte';
    import prediction from "$lib/Store.js";
    import varieties from "$lib/varieties.js"

    let predictedCrop = '';
    let compactibility = '';
    let returnedVarieties = [];
    let isLoading = false;

    onMount(() => {
        prediction.subscribe(value => {
            predictedCrop = value.prediction; 
            compactibility = value.compactibility;
            console.log(predictedCrop, "score is", compactibility);
        });

        varieties.subscribe(crops => {
            returnedVarieties = crops; 
            console.log(returnedVarieties);
            console.log("size",returnedVarieties.length <= 0)
        });
    });
</script>

{#if returnedVarieties.length <= 0}
    <div class="prediction-section">
        <p class="prediction-text">We have recommended:</p>
        <p class="prediction-result">{predictedCrop}</p>
        <p class="prediction-text">Compactibility:</p>
        <small class="prediction-result">{compactibility}</small>
        <p class="prediction-text">That is all we can do for now</p>
    </div>
{:else}
<p>That is all we can do</p>
{/if}

<style>
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
</style>
