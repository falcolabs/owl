<script lang="ts">
    import type { Readable } from "svelte/store";
    import PillTag from "./PillTag.svelte";
    import TextAnswerColored from "./TextAnswerColored.svelte";
    import { PlayerManager, StateManager } from "$lib";

    export let states: StateManager;
    export let players: PlayerManager;

    console.log($states.answers);
</script>

<div class="container">
    {#if $states.answers !== undefined && $states.engine_players.size != 0}
        {#each $states.answers as { time, name, content, verdict }}
            <TextAnswerColored
                {time}
                name={PlayerManager.getDisplayName(name, $states.engine_players)}
                {content}
                {verdict}
            />
        {/each}
    {/if}
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        gap: 70px;
    }
</style>
