<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure, GameMaster } from "$lib";
    import type { Timer, Player } from "client";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    import SubmitJudger from "./SubmitJudger.svelte";
    import Load from "../Load.svelte";
    export let states: StateManager;
    export let conn: Connection;
</script>

<Load until={$states.media !== undefined}>
    <div class="horizontal big-gap">
        <div class="vertical big-gap">
            <div class="nofat">
                <p class="code">Question #{$states.qid + 1}. {$states.prompt}</p>
            </div>
            <div>
                <h1>Display Controls</h1>
                <button
                    class="btn"
                    class:accent={$states.show_key}
                    on:click={async () => {
                        await states.setBoolean("show_key", !$states.show_key);
                    }}>{$states.show_key ? "Keys Shown" : "Keys Hidden"}</button
                >
            </div>
            <div class="vertical big-gap">
                <h1>Media Controls</h1>
                {#if $states.media !== null}
                    <div class="horizontal">
                        <button
                            class="btn smol"
                            class:accent={$states.media_status.visible}
                            on:click={async () => {
                                let status = $states.media_status;
                                status.visible = !status.visible;
                                await states.setObject("media_status", status);
                            }}>{$states.media_status.visible ? "Shown" : "Hidden"}</button
                        >
                        {#if $states.media.mediaType == "video"}
                            <button
                                class="btn smol"
                                class:accent={!$states.media_status.playbackPaused}
                                on:click={async () => {
                                    let status = $states.media_status;
                                    status.playbackPaused = !status.playbackPaused;
                                    await states.setObject("media_status", status);
                                }}
                                >{$states.media_status.playbackPaused
                                    ? "Paused"
                                    : "Playing"}</button
                            >
                        {/if}
                    </div>
                {:else}
                    No media available for this question.
                {/if}
            </div>
            <div class="vertical big-gap">
                <h1>Question Controls</h1>
                <div class="horizontal">
                    {#each [41, 42, 43, 44] as qi}
                        <button
                            class="btn smol code"
                            class:accent={$states.qid == qi}
                            on:click={async () => {
                                let status = $states.media_status;
                                status.playbackPaused = true;
                                await states.setObject("media_status", status);
                                await states.setNumber("qid", qi);
                            }}>{qi}</button
                        >
                    {/each}
                </div>
            </div>
        </div>
        <SubmitJudger {conn} {states} prefix="tangtoc" />
    </div>
</Load>

<style>
    .nofat {
        max-width: 30vw;
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

    div.big-gap {
        gap: 15px;
    }

    .vertical {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .horizontal {
        display: flex;
        flex-direction: row;
        gap: 5px;
    }

    .accent {
        background-color: var(--accent);
    }

    .smol {
        padding: 15px;
        margin: 0;
        font-size: 1em;
        border-radius: 9px;
        border: none;
    }

    .code {
        font-family: var(--font-monospace);
    }
</style>
