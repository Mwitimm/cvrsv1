<script>
    import Tabs from "$lib/Tabs.svelte"
    import Allwecan from "$lib/Allwecan.svelte"

    import Start from "$lib/Start.svelte"

    let somelinks = ["profile","recs","other"]

    let active = somelinks[1]

    const tabChange = (e) => {active =  e.detail};
  
  </script>
  
  
<!--  <section>
    <Tabs {active}{somelinks} on:tabChange={tabChange}/>
  </section>-->
 <!-- {#if active ===  somelinks[0]}
  <p>Show profile page</p>
  {:else if active === somelinks[1]} 
  <p>Show Reccomendations</p>
{:else}
<p>
    show some other staff
</p>
  
  {/if}-->  
<Allwecan/>




