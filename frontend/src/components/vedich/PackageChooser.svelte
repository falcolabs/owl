<script lang="ts">
    import { type Readable } from "svelte/store";
    import Load from "../Load.svelte";

    export let states: Readable<any>;
</script>

<div class="container">
    {#if $states.current_player_username !== ""}
        {#each [0, 1, 2] as i}
            <div class="line">
                <div
                    class="prompt pillbutton left"
                    class:activated={$states.package[$states.current_player_username][i] == 20}
                >
                    20
                </div>
                <div
                    class="prompt pillbutton right"
                    class:activated={$states.package[$states.current_player_username][i] == 30}
                >
                    30
                </div>
            </div>
        {/each}
    {/if}
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        gap: 25px;
    }

    .activated {
        background-color: var(--border-color);
    }

    .pillbutton.left {
        border-radius: var(--radius-2) 0 0 var(--radius-2);
    }

    .pillbutton.right {
        border-radius: 0 var(--radius-2) var(--radius-2) 0;
    }

    .pillbutton {
        font-weight: bold;
        min-width: 7.5rem;
        padding: 25px;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 1px solid var(--border-color);
    }

    .line {
        border-radius: var(--radius-2);
        background-color: var(--slate-1);
        border: var(--border);
        min-width: 15rem;
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        font-weight: bold;
        box-shadow: var(--shadow-s);
    }
</style>
