<script lang="ts">
    import { writable } from "svelte/store";
    import TitleBar from "../TitleBar.svelte";
    import ShowAnswer from "../ShowAnswer.svelte";
    import { onMount } from "svelte";
    import { Peeker, Connection, GameMaster, StateManager, CallProcedure } from "$lib";
    import Load from "../Load.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";
    import BareTimer from "../BareTimer.svelte";

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
    let timerStore = states.timerStore;
    export let conn: Connection;
    export let gm: GameMaster;
    export let players: PlayerManager;
    let videoElement: HTMLVideoElement;
    let audioElement: HTMLAudioElement;
    let imageElement: HTMLImageElement;
    let previousState = 0;
    let videoProgress = writable(1);
    let blobs: { [key: string]: string } = {};
    let answer: string;
    let timeElapsed = 30;
    let hasMine = false;
    let timer = states.timerStore;

    onMount(async () => {
        // @ts-ignore
        states.on("preload_list", (l: any) => {
            Object.entries(l).forEach(async (a) => {
                let qn = JSON.parse(a[0]);
                // @ts-ignore
                let media = JSON.parse(a[1]);
                if (media == null) return;
                console.log("uri is", media);
                let r = await fetch(media.uri);
                blobs[media.uri] = URL.createObjectURL(await r.blob());
            });
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
                            states.setTimer(new Peeker.Timer());
                        }
                        await videoElement.play();
                        $timerStore.resume();

                        videoElement.onended = (ev) => {
                            states.setTimer(new Peeker.Timer());
                            states.setObject("media_status", {
                                visible: true,
                                playbackPaused: true
                            });
                            videoProgress.set(0);
                        };
                    }
                } else {
                    videoElement?.pause();
                    $timerStore.pause();
                }
                states.setTimer($timerStore);
            }
            previousState = s.media_status.playbackPaused;
        });

        states.subscribe((s: any) => {
            if (s.answers === undefined) {
                hasMine = false;
                return;
            }
            for (let ans of s.answers) {
                if (ans.name == gm.username && ans.content != "" && ans.time != 30) {
                    hasMine = true;
                    return;
                }
            }
            hasMine = false;
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
                <div class="sep">
                    <div class="sepleft">
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
                                        class="mmedia mobj"
                                        bind:this={videoElement}
                                        src={blobs[$states.media.uri]}
                                    />
                                {:else if $states.media.mediaType == "image"}
                                    <img
                                        class="mmedia mobj"
                                        src={blobs[$states.media.uri]}
                                        alt="Question content"
                                        bind:this={imageElement}
                                    />
                                {:else if $states.media.mediaType == "audio"}
                                    <audio
                                        class="mmedia mobj"
                                        src={blobs[$states.media.uri]}
                                        bind:this={audioElement}
                                    />
                                {/if}
                            {:else}
                                <div class="media-placeholder" />
                            {/if}
                        </div>
                        <div class="timer"><BareTimer progress={videoProgress} /></div>
                    </div>
                    <div class="sepright">
                        <div>
                            <div class="answergroup">
                                <p class="reminder">Bấm Enter để gửi</p>
                                {#if $timer.isPaused()}
                                    <p class="reminder">Đồng hồ không chạy</p>
                                {:else if hasMine}
                                    <p class="reminder">
                                        Đã nộp lúc <span class="code">{timeElapsed.toFixed(2)}</span
                                        >s
                                    </p>
                                {:else}
                                    <p class="reminder">Chưa nộp</p>
                                {/if}
                            </div>
                            <form
                                on:submit|preventDefault={async () => {
                                    if ($timer.isPaused()) {
                                        return;
                                    }
                                    timeElapsed = $timer.elapsedSecs();
                                    await conn.send(
                                        CallProcedure.name("tangtoc::submit_answer")
                                            .string("answer", answer)
                                            // @ts-ignore
                                            .string("token", gm.authToken)
                                            .number("time", timeElapsed)
                                            .build()
                                    );
                                }}
                            >
                                <input
                                    class="inp"
                                    type="text"
                                    placeholder="Nhập đáp án"
                                    spellcheck="false"
                                    bind:value={answer}
                                />
                            </form>
                        </div>
                    </div>
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

    .sep {
        display: flex;
        flex-direction: row;
        gap: 15px;
    }

    .sepleft {
        display: flex;
        flex-direction: column;
        gap: 15px;
        align-items: center;
    }

    .sepright {
        padding: 15px 25px;
        width: 30vw;
        display: flex;
        flex-direction: column-reverse;
        height: calc(100% - 2rem);
        justify-content: space-between;
    }

    .inp {
        width: 100%;
    }

    .answergroup {
        color: var(--text-2);
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 10px;
    }

    .code {
        font-family: var(--font-monospace);
    }
</style>
