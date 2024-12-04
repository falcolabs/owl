<script lang="ts">
    import { CallProcedure, Connection, GameMaster, StateManager } from "$lib";
    import type { Timer } from "client";
    import { type Readable, type Writable } from "svelte/store";

    export let conn: Connection;
    export let gm: GameMaster;
    export let states: StateManager;
    export let elapsed: Readable<any>;
</script>

<div>
    <h1>Bộ đếm giờ</h1>
    <p>
        Time Left: <span class="code"
            >{$states.timer_paused ? "(PAUSED)" : "(RUNNING)"}&nbsp{$elapsed}</span
        >
    </p>
    <div class="bgroup-hor">
        {#if $elapsed === "0"}
            {#each ["reset", "pause"] as ops}
                <button
                    on:click={async () => {
                        // @ts-ignore
                        await gm.timer_operation(ops);
                    }}
                    class="btn"
                >
                    {ops == "start" ? "chạy" : ops == "pause" ? "tạm dừng" : "đặt lại"}
                </button>
            {/each}
        {:else}
            {#each ["start", "pause", "reset"] as ops}
                <button
                    on:click={async () => {
                        // @ts-ignore
                        await gm.timer_operation(ops);
                    }}
                    class="btn"
                >
                    {ops == "start" ? "chạy" : ops == "pause" ? "tạm dừng" : "đặt lại"}
                </button>
            {/each}
        {/if}
    </div>
</div>

<style>
    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1rem;
        margin: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--bg-dark-2);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: fit-content;
    }

    .code {
        font-family: var(--font-monospace);
    }

    .btn:hover {
        filter: brightness(120%);
    }

    h1 {
        font-size: var(--font-normal);
        font-weight: bold;
        width: fit-content;
        margin-bottom: 1rem;
    }
</style>
