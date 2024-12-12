<script lang="ts">
    import { CallProcedure, Connection, GameMaster, StateManager } from "$lib";
    import type { Timer } from "client";
    import { onMount } from "svelte";
    import { writable, type Readable, type Writable } from "svelte/store";

    export let gm: GameMaster;
    export let onstart: () => Promise<void> = async () => {};
    export let onpause: () => Promise<void> = async () => {};
    export let onreset: () => Promise<void> = async () => {};

    let states = gm.states;
    let time = states.time;
    let elapsed = writable("");
    onMount(() => {
        setInterval(async () => {
            let e = $time;
            if ($states.max_time !== undefined) {
                if ($states.max_time - e <= 0) {
                    $elapsed = "0";
                    if (!$states.timer_paused) {
                        await gm.timer_operation("pause");
                    }
                } else {
                    $elapsed = ($states.max_time - e).toFixed(2);
                }
            } else {
                $elapsed = `Video progress: ${e.toFixed(2)}`;
            }
        }, 100);
    });
</script>

<div>
    <h1>Bộ đếm giờ</h1>
    <p>
        Time Left: <span class="code"
            >{$states.timer_paused ? "(PAUSED)" : "(RUNNING)"}&nbsp{$elapsed}</span
        >
    </p>
    <div class="bgroup-hor">
        {#if $elapsed !== "0"}
            <button
                class:accent={!$states.timer_paused}
                on:click={async () => {
                    // @ts-ignore
                    await gm.timer_operation($states.timer_paused ? "start" : "pause");
                    $states.timer_paused ? await onstart() : await onpause()
                }}
                class="btn"
            >
                {$states.timer_paused ? "chạy" : "dừng"}
            </button>
        {/if}
        <button
            on:click={async () => {
                // @ts-ignore
                await gm.timer_operation("reset");
                await onreset();
            }}
            class="btn"
        >
            đặt lại
        </button>
    </div>
</div>

<style>
    .code {
        font-family: var(--font-monospace);
    }

    .bgroup-hor {
        display: flex;
        flex-direction: row;
        gap: 15px;
    }

    h1 {
        font-size: var(--font-normal);
        font-weight: bold;
        width: fit-content;
        margin-bottom: 1rem;
    }
</style>
