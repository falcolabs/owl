<script lang="ts">
    import ScorePill from "./ScorePill.svelte";

    export let states;
</script>

<div class="bar">
    {#if $states.highlighted !== undefined}
        {#each $states.engine_players as player}
            <ScorePill
                activated={$states.highlighted.includes(player.identifier)}
                name={player.name}
                score={player.score}
            />
        {/each}
    {/if}
</div>

<style>
    .bar {
        display: flex;
        flex-direction: row;
        gap: 25px;
        width: fit-content;
        justify-content: flex-start;
        align-items: flex-start;
    }
</style>
