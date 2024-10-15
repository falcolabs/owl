<script lang="ts">
    import { type Readable, readable, writable } from "svelte/store";
    import TitleBar from "../TitleBar.svelte";
    import ShowAnswer from "../ShowAnswer.svelte";
    import { onMount } from "svelte";
    import { Peeker, Connection, GameMaster } from "$lib";
    import Load from "../Load.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";

    export let states: Readable<any> = writable({
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
    export let conn: Connection;
    export let gm: GameMaster;
    export let players: PlayerManager;
    let videoElement: HTMLVideoElement;
    let audioElement: HTMLAudioElement;
    let imageElement: HTMLImageElement;
    let previousState = 0;

    onMount(async () => {
        states.subscribe(async (s) => {
            if (!s.__init) return;
            if (s.media_status.playbackPaused === previousState) return;
            if (s.media === null) return;
            if (s.media.mediaType == "video") {
                if (!s.media_status.playbackPaused) {
                    if (videoElement.paused) {
                        await videoElement?.play();
                    }
                } else {
                    videoElement?.pause();
                }
            }
            previousState = s.media_status.playbackPaused;
        });
    });
</script>

<title>Tăng tốc - Đường đua xanh</title>
<div class="bg spcbtwn">
    <TitleBar activity="Tăng tốc" />
    <Load until={gm !== undefined && $states.__init}>
        <div class="center-box upper">
            {#if $states.show_key}
                <ShowAnswer {states} />
            {:else}
                <div class="padded box mmedia">
                    <p class="prompt midalign">{$states.prompt}</p>
                </div>
                <div class="box vp">
                    {#if $states.media == null}
                        <div class="media-placeholder" />
                    {:else if $states.media_status.visible}
                        {#if $states.media.mediaType == "video"}
                            <!-- svelte-ignore a11y-media-has-caption -->
                            <video
                                class="mmedia"
                                bind:this={videoElement}
                                src={$states.media.uri}
                            />
                        {:else if $states.media.mediaType == "image"}
                            <img class="mmedia" src={$states.media.uri} alt="Question content" />
                        {:else if $states.media.mediaType == "audio"}
                            <img class="mmedia" src={$states.media.uri} alt="Question content" />
                        {/if}
                    {:else}
                        <div class="media-placeholder" />
                    {/if}
                </div>
                <div class="timer">timer</div>
            {/if}
        </div>
        <div class="scorebar"><ScoreBar {players} {states} /></div>
    </Load>
</div>

<style>
    .media-placeholder {
        min-width: calc(50vw + 80px);
        min-height: calc(50vh + 80px);
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
        margin-top: -10px;
    }

    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .mmedia {
        width: calc(50vw + 80px);
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
