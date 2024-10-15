<script lang="ts">
    import type { Readable } from "svelte/store";
    import PillTag from "./PillTag.svelte";
    import TextAnswer from "./TextAnswer.svelte";

    export let states: Readable<any>;
</script>

<div class="container">
    {#each $states.answers as {time, name, content, verdict}}
        <TextAnswer {time} {name} {content} {verdict} />
    {/each}
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        gap: 70px;
    }
</style>
