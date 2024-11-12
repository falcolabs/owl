<script lang="ts">
    import type { Readable } from "svelte/store";
    import PillTag from "./PillTag.svelte";
    import TextAnswer from "./TextAnswer.svelte";
    import type { PlayerManager } from "$lib";

    export let states: Readable<any>;
    export let players: PlayerManager;
</script>

<div class="container">
    {#if $states.answers !== undefined && players.storage.size != 0}
        {#each $states.answers as { time, name, content, verdict }}
            <TextAnswer {time} name={players.name(name).name} {content} {verdict} />
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
