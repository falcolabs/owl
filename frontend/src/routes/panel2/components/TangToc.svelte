<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure, GameMaster } from "$lib";
    import type { Timer, Player } from "client";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    import SubmitJudger from "./SubmitJudger.svelte";
    import Load from "../../../components/Load.svelte";
    import TimerControls from "./TimerControls.svelte";
    export let gm: GameMaster;
    export let states: StateManager;
    export let conn: Connection;

    let time = states.time;
</script>

<Load until={$states.media !== undefined}>
    <div class="horizontal big-gap">
        <div class="vertical big-gap">
            <div>
                <h1>Game Master</h1>
                <div class="horizontal">
                    <button
                    class="btn"
                    class:accent={$states.show_key}
                    on:click={async () => {
                        if (!$states.show_key) {
                            await gm.sound.play("tangtoc-showanswers");
                            console.log("1.5s delay before showing answer");
                            setTimeout(async () => {
                                await states.setBoolean("show_key", !$states.show_key);
                            }, 1500);
                        } else {
                            await states.setBoolean("show_key", !$states.show_key);
                        }
                    }}>{$states.show_key ? "ĐÁ thí sinh: HIỆN" : "ĐÁ thí sinh: ẨN"}</button
                >
                <button
                    class="btn"
                    class:accent={$states.reveal_answer}
                    on:click={async () =>
                        await states.setBoolean("reveal_answer", !$states.reveal_answer)}
                    >Hiện đáp án</button
                >
                </div>
            </div>
            <TimerControls
                {gm}
                onstart={async () => {
                    switch ($states.max_time) {
                        case 10:
                            await gm.sound.play("tangtoc-10secs");
                            break;
                        case 20:
                            await gm.sound.play("tangtoc-20secs");
                            break;
                        case 30:
                            await gm.sound.play("tangtoc-30secs");
                            break;
                        case 40:
                            await gm.sound.play("tangtoc-40secs");
                            break;
                    }
                }}
            />
            <div class="vertical big-gap">
                <h1>Đa phương tiện</h1>
                {#if $states.media !== null}
                    <div class="horizontal">
                        <button
                            class="btn smol"
                            class:accent={$states.media_status.visible}
                            on:click={async () => {
                                let status = $states.media_status;
                                status.visible = !status.visible;
                                await states.setObject("media_status", status);
                            }}>{$states.media_status.visible ? "Ẩn" : "Hiện"}</button
                        >
                        {#if $states.media.mediaType == "video"}
                            <button
                                class="btn smol"
                                class:accent={!$states.media_status.playbackPaused}
                                on:click={async () => {
                                    let status = $states.media_status;
                                    status.playbackPaused = !status.playbackPaused;
                                    if (status.playbackPaused) {
                                        await gm.sound.stop("tangtoc-40secs");
                                        await gm.timer_operation("pause");
                                    } else {
                                        await gm.sound.play("tangtoc-40secs");
                                        await gm.timer_operation("start");
                                    }
                                    await states.setObject("media_status", status);
                                }}
                                >{$states.media_status.playbackPaused
                                    ? "Khồng chạy"
                                    : "Đang chạy"}</button
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
                    <button
                        class="btn smol nomargin-horizontal"
                        class:accent={$states.qid == -1}
                        on:click={async () => await states.setNumber("qid", -1)}>unset</button
                    >
                    {#each [42, 43, 44, 45] as qi}
                        <button
                            class="btn smol code"
                            class:accent={$states.qid == qi}
                            on:click={async () => {
                                let status = $states.media_status;
                                status.playbackPaused = true;
                                await states.setObject("media_status", status);
                                await states.setNumber("qid", qi);
                                await gm.sound.play("tangtoc-revealquestion");
                            }}>{qi}</button
                        >
                    {/each}
                </div>
            </div>
            <div class="nofat">
                <p>Câu {$states.qid + 1}. {$states.prompt}</p>
                <p style="font-weight: bold;">{$states.key}</p>
            </div>
        </div>
    </div>
</Load>

<style>
    h1 {
        font-weight: bold;
    }
    .nofat {
        max-width: 30vw;
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

    .code {
        font-family: var(--font-monospace);
    }
</style>
