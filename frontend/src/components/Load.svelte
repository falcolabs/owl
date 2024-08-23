<script lang="ts">
    export let until: boolean;
</script>

<div>
    {#if until}
        <slot>Passed Guard.</slot>
    {:else}
        <h1>Loading...</h1>
    {/if}
</div>
