<script lang="ts">
    import type { StateManager } from "$lib";
    import Load from "./Load.svelte";
    import ScorePill from "./ScorePill.svelte";

    export let states: StateManager;
</script>

<Load until={$states.engine_players !== undefined}>
    <div class="bar">
        {#if $states.highlighted !== undefined}
            {#each $states.engine_players as player}
                <ScorePill
                    activated={$states.highlighted.includes(player.identifier)}
                    name={player.name}
                    score={player.score}
                />
            {/each}
        {:else}
            {#each $states.engine_players as player}
                <ScorePill activated={false} name={player.name} score={player.score} />
            {/each}
        {/if}
    </div>
</Load>

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
