<script lang="ts">
    import { CallProcedure, GameMaster, PlayerManager, StateManager, type Connection } from "$lib";
    import { onMount } from "svelte";

    export let gm: GameMaster;
    export let identifier: string;
    let inp: number;
</script>

<form
    on:submit={async () => {
        if (inp == null || inp == undefined) return;
        await gm.set_score(identifier, inp);

        // @ts-ignore
        inp = undefined;
    }}
>
    <input type="number" class="scoreset" bind:value={inp} />
</form>

<style>
    .scoreset {
        border-radius: 9px;
        border: solid 2px #6a72b4;
        background-color: #434a82;
        padding: 10px 15px;
        color: var(--text);
        font-family: var(--font);
        font-weight: bold;
        font-size: var(--font-normal);
        transition: 100ms ease-in;
        width: 10rem;
    }

    .scoreset:hover,
    .scoreset:focus {
        outline: none;
        border: solid 2px var(--accent);
    }
</style>
