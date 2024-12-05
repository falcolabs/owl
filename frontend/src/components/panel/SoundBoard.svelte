<script lang="ts">
    import type { GameMaster } from "$lib";
    import type { AvailableSound } from "client";
    import Load from "../Load.svelte";

    export let sounds: { displayName: string; fileName: AvailableSound }[];
    export let gm: GameMaster;

    let states = gm.states;
</script>

<div class="container">
    <Load until={$states.active_sounds !== undefined}>
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
                    console.log($states.active_sounds);
                    // @ts-ignore
                    // prevents space bar or enter from triggering the button
                    ev.target?.blur();
                }}>{sound.displayName}</button
            >
        {/each}
    </Load>
</div>

<style>
    .sboardbtn {
        width: 170px;
        height: 170px;
    }

    .btn {
        margin: 0.5rem;
    }

    .accent {
        background-color: var(--accent);
    }
</style>
