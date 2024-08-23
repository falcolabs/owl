<script lang="ts">
    import ScorePill from "./ScorePill.svelte";
    import { GameMaster } from "$lib";

    export let gamemaster: GameMaster;
    let { players, states } = gamemaster;
</script>

<div class="bar">
    {#each $players as [_, player]}
        <ScorePill
            activated={$states.seperated_candidate == player.identifier}
            name={player.name}
            score={player.score}
        />
    {/each}
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
