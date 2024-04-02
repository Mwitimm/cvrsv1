<script>

    import Navigation from "$lib/Navigation.svelte"
    import Specific   from "$lib/Specific.svelte"
</script>
<section class="nav">
    <Navigation/>
</section>
<section class="specific">
<Specific/>
</section>

<style>
    .nav{
        z-index: 1;
        position: fixed;
        padding: 0;
        margin: 0;
 
    }
    .specific{
      
        background-color: #008000;
    }
</style>