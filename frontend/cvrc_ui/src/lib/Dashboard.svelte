<script>

    import Navigation from "$lib/Navigation.svelte"
    import Specific   from "$lib/Specific.svelte"
    import Sidebar   from "$lib/Sidebar.svelte"
    import Updateprofile   from "$lib/Updateprofile.svelte"
    import Farms from "$lib/Farms.svelte"
    import prediction from "$lib/Store.js";
    import Start from "$lib/Start.svelte"
    import Allwecan from "$lib/Allwecan.svelte"
    import { onMount } from 'svelte';
 
let components =["recommendations","profile","farms"]
 let activeComponent = components[0]

 const tabChange = (e) => {activeComponent =  e.detail};


 

 let predictedCrop = '';
 let compactibility = ''
 let returnedVarieties


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

 

 });


</script>
<section class="nav">
    <Navigation/>
</section>
<section class="sidebar">
    <Sidebar  {activeComponent} {components} on:tabChange={tabChange}/>
</section>

{#if activeComponent ===  components[0]}


<section class="specific">

<Specific/>



</section>


{:else if activeComponent ===  components[1]}
<section class="profile">
<Updateprofile/>
</section>


{:else if activeComponent ===  components[2]}
<section class="farms">
<Farms/>
</section> 


  
 
  {/if}



<style>
    .nav{
        z-index: 1;
        position: fixed;
        padding: 0;
        margin: 0;
 
    }
    .specific{
        margin-left: 16%;
      
        background-color: #008000;
    }
    .profile{

        margin-left: 16%;

    }
    .farms{
        margin-left: 16%;
    }
</style>