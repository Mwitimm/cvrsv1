<script>

    import { createEventDispatcher } from 'svelte';
    let dispatch = createEventDispatcher();
export let somelinks
export let active




</script>

<div class="tabs">
  <ul>
  {#each somelinks as links}
  <li  on:click={() => dispatch('tabChange', links)} >

  <div class:active={links === active}>
    {links}
  </div>

  </li>
  {/each}
  </ul>
</div>

<style>
  li{
    cursor:arrow;
  }  
.active{
background:green;
}
</style>