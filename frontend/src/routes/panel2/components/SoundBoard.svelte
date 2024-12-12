<script lang="ts">
    import type { GameMaster } from "$lib";
    import type { AvailableSound } from "client";
    import Load from "../../../components/Load.svelte";

    export let sounds: { displayName: string; fileName: AvailableSound }[];
    export let gm: GameMaster;

    let states = gm.states;
</script>

<Load until={$states.active_sounds !== undefined}>
    <div class="container">
        {#each sounds as sound}
            <button
                class="btn sboardbtn"
                class:accent={$states.active_sounds.includes(sound.fileName)}
                on:click={async (ev) => {
                    if (!$states.active_sounds.includes(sound.fileName)) {
                        // @ts-ignore
                        await gm.sound.play(sound.fileName);
                    } else {
                        // @ts-ignore
                        await gm.sound.stop(sound.fileName);
                    }
                    // @ts-ignore
                    // prevents space bar or enter from triggering the button
                    ev.target?.blur();
                }}><p>{sound.displayName}</p></button
            >
        {/each}
    </div>
</Load>

<style>
    .container {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        gap: 15px;
    }

    .sboardbtn {
        width: 170px;
        padding: 1rem;
        height: 170px;
        text-wrap: wrap;
    }

    .accent {
        background-color: var(--accent);
    }
</style>
