<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure } from "$lib";
    import Load from "../Load.svelte";

    export let states: StateManager;
    export let conn: Connection;
</script>

<div>
    <h1>Chỉnh phần</h1>
    <Load until={$states.available_parts !== undefined}>
        <div class="horizontal">
            <div class="horizontal parts">
                {#each Object.entries($states.available_parts) as [index, name]}
                    <button
                        class="btn smol"
                        class:accent={$states.current_part == index}
                        on:click={async () => {
                            await states.setNumber("current_part", Number(index));
                        }}>{name}</button
                    >
                {/each}
            </div>
            <button
                class="btn smol bfreeze"
                class:accent={!$states.engine_freeze}
                on:click={async () => {
                    await states.setBoolean("engine_freeze", !$states.engine_freeze);
                }}>{$states.engine_freeze ? "Đóng băng" : "Trực tiếp"}</button
            >
        </div>
    </Load>
</div>

<style>
    h1 {
        font-size: var(--font-normal);
        font-weight: bold;
        width: fit-content;
        margin-bottom: 1rem;
    }

    .horizontal {
        display: flex;
        flex-direction: row;
        gap: 5px;
        height: max-content;
    }

    .parts {
        width: 70%;
        flex-wrap: wrap;
    }

    .bfreeze {
        height: fit-content;
    }

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

    .btn:hover {
        filter: brightness(120%);
    }

    .smol {
        padding: 15px;
        margin: 0;
        font-size: 1em;
        border-radius: 9px;
        border: none;
    }

    .accent {
        background-color: var(--accent);
    }
</style>
