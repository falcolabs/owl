<script lang="ts">
    import { CallProcedure, Connection } from "$lib";
    import { type Readable } from "svelte/store";

    export let conn: Connection;
    export let elapsed: Readable<any>;
</script>

<div>
    <p>Time Elapsed: <span class="code">&nbsp{$elapsed}</span></p>
    <div class="bgroup-hor">
        {#each ["start", "pause", "reset"] as ops}
            <button
                on:click={async () => {
                    await conn.send(
                        CallProcedure.name("engine::timer_operation")
                            .string("operation", ops)
                            .build()
                    );
                }}
                class="btn"
            >
                {ops}
            </button>
        {/each}
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
</style>
