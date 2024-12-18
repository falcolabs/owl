<script lang="ts">
    import { type Readable, readable, writable } from "svelte/store";
    import TitleBar from "../TitleBar.svelte";
    import ShowAnswer from "../ShowAnswer.svelte";
    import { onMount } from "svelte";
    import {
        Peeker,
        Connection,
        GameMaster,
        StateManager,
        CallProcedure,
        AssetManager
    } from "$lib";
    import Load from "../Load.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";
    import BareTimer from "../BareTimer.svelte";
    import TimerBar from "../TimerBar.svelte";

    // @ts-ignore
    export let states: StateManager = writable({
        prompt: "Sắp xếp các hình minh họa vào vị trí tương ứng để hoàn thiện sơ đồ quá trình nguyên phân ở tế bào động vật",
        media: { media_type: "video", uri: "testvid.mp4" },
        show_key: false,
        media_status: { visible: false, playback_paused: true },
        answers: [
            { time: 29.5, name: "MrBeast", content: "IELT", verdict: null },
            { time: 1.3, name: "Joe Biden", content: "O-O-O", verdict: true },
            { time: 69.42, name: "Trump", content: "d4d5", verdict: false },
            { time: 2, name: "herobrine", content: "sasfsf", verdict: null }
        ]
    });
    export let gm: GameMaster;
    export let players: PlayerManager;
    export let assets: AssetManager;
    let videoElement: HTMLVideoElement;
    let audioElement: HTMLAudioElement;
    let imageElement: HTMLImageElement;
    let previousState = 0;
    let videoProgress = writable(1);
    let assetURL = writable("");

    onMount(async () => {
        // @ts-ignore
        states.on("media", async ({ uri }) => {
            if (uri == null) {
                $assetURL = "";
                return;
            }
            $assetURL = await assets.getURL(uri);
        });

        states.subscribe(async (s) => {
            if (!s.__init || s.media_status === undefined) return;
            if (s.media_status.playbackPaused === previousState) return;
            if (s.media === null || s.media === undefined) return;
            if (s.media.mediaType == "video") {
                if (videoElement == null) return;
                if (!s.media_status.playbackPaused) {
                    if (videoElement.paused) {
                        if (videoElement.currentTime == 0) {
                            gm.timer_operation("reset");
                        }
                        await videoElement.play();
                        await gm.timer_operation("start");

                        videoElement.onended = (ev) => {
                            gm.timer_operation("reset");

                            states.setObject("media_status", {
                                visible: true,
                                playbackPaused: true
                            });
                            videoProgress.set(0);
                        };
                    }
                } else {
                    videoElement?.pause();
                    await gm.timer_operation("pause");
                }
            }
            previousState = s.media_status.playbackPaused;
        });

        setInterval(() => {
            if (videoElement === null || videoElement === undefined) return;
            videoProgress.set(1 - videoElement.currentTime / videoElement.duration);
        }, 100);
    });
</script>

<title>Tăng tốc - Đường đua xanh</title>
<div class="bg spcbtwn">
    <TitleBar activity="Tăng tốc" />
    <Load until={gm !== undefined && $states.__init}>
        <div class="center-box upper">
            {#if $states.show_key}
                <ShowAnswer {states} {players} />
            {:else}
                <div class="padded box mmedia">
                    <p class="prompt midalign">{$states.prompt}</p>
                </div>
                <div class="box vp">
                    {#if $states.media == null}
                        <div class="media-placeholder" />
                    {:else if $states.media_status.visible && $assetURL !== ""}
                        {#if $states.media.mediaType == "video"}
                            <!-- svelte-ignore a11y-media-has-caption -->
                            <video class="mmedia mobj" bind:this={videoElement} src={$assetURL} />
                        {:else if $states.media.mediaType == "image"}
                            <img
                                class="mmedia mobj"
                                src={$assetURL}
                                alt="Question content"
                                bind:this={imageElement}
                            />
                        {:else if $states.media.mediaType == "audio"}
                            <audio class="mmedia mobj" src={$assetURL} bind:this={audioElement} />
                        {/if}
                    {:else}
                        <div class="media-placeholder" />
                    {/if}
                </div>
                <div class="timer">
                    {#if $states.media != null}
                        {#if $states.media.mediaType == "video"}
                            <BareTimer progress={videoProgress} />
                        {:else}
                            <TimerBar {states} />
                        {/if}
                    {/if}
                </div>
            {/if}
        </div>
        <div class="scorebar"><ScoreBar {states} /></div>
    </Load>
</div>

<style>
    .vp {
        background: #000000;
        min-width: calc(50vw + 80px);
        min-height: calc(50vh + 80px);
    }
    .mmedia {
        max-width: calc(50vw + 80px);
        width: calc(50vw + 80px);
    }

    .scorebar {
        width: 100vw;
        display: flex;
        justify-content: center;
    }

    .spcbtwn {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .timer {
        width: calc(50vw + 40px);
        margin-top: -10px;
    }

    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .mobj {
        min-width: calc(50vw + 80px);
        min-height: 50vh;
    }

    .box {
        overflow: hidden;
    }

    .upper {
        gap: 25px;
    }

    .midalign {
        text-align: center;
    }

    .padded {
        padding: 20px 40px;
        max-width: 50vw;
    }

    .center-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: calc(100vh - 5rem);
        flex-direction: column;
        transform: translateY(2rem);
    }
</style>
