<script lang="ts">
    import VcnvLine from "../vcnv/VCNVLine.svelte";
    import PillTag from "../PillTag.svelte";
    import { CallProcedure, GameMaster, type Connection, type StateManager } from "$lib";
    import { writable, type Writable } from "svelte/store";
    import TimerBar from "../TimerBar.svelte";
    import { onMount } from "svelte";

    export let conn: Connection;
    export let gm: GameMaster;
    export let states: StateManager;

    let answer: string;
    let timer = states.timerStore;
    let timeElapsed = 30;
    let inputBox: HTMLInputElement;
    let lines = writable(
        new Map<string, Writable<{ status: string; content: string; tag: string }>>()
    );
    states.subscribe((s) => {
        console.log("checking");
        if (s.puzzle_data == undefined) return;
        console.log("passed checkpoint1", s);
        if (s.final_hint) {
            if ($lines.size != 1) {
                console.log("M");
                let o = new Map();
                o.set(s.puzzle_data.center.tag, writable(s.puzzle_data.center));
                lines.set(o);
            } else {
                $lines.get(s.puzzle_data.center.tag)?.set(s.puzzle_data.center);
            }
        } else {
            if ($lines.size != 4) {
                let o = new Map();
                for (let entry of $states.puzzle_data.normal) {
                    o.set(entry.tag, writable(entry));
                }

                lines.set(o);
            } else {
                for (let entry of $states.puzzle_data.normal) {
                    $lines.get(entry.tag)?.set(entry);
                }
            }
        }
    });

    let hasMine = false;

    onMount(() => {
        inputBox.focus();
        timer.subscribe((t) => {
            try {
                if (!t.isPaused()) {
                    inputBox.focus();
                }
            } catch (e) {}
        });
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
</script>

<div class="top">
    <div class="left">
        <div class="up box">
            {#each $lines as [_, line]}
                <VcnvLine {line} />
            {/each}
        </div>
        <div class="qbox box">
            <div class="ptag">
                <PillTag text={$states.selected != "" ? "Hàng " + $states.selected : "Lựa chọn"} />
            </div>
            <p class="prompt">{$states.prompt}</p>
            <div>
                <div class="answergroup">
                    <p class="reminder">Bấm Enter để gửi</p>
                    {#if $timer.isPaused()}
                        <p class="reminder">Chưa đếm ngược</p>
                    {:else if hasMine}
                        <p class="reminder">
                            Đã nộp lúc <span class="code">{timeElapsed.toFixed(2)}</span>s
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
                            CallProcedure.name("vcnv::submit_answer")
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
                        bind:value={answer}
                        bind:this={inputBox}
                        type="text"
                        placeholder="Nhập đáp án"
                        spellcheck="false"
                    />
                </form>
                <div class="timerbar"><TimerBar {states} /></div>
            </div>
        </div>
    </div>
    <div class="picontainer">
        <div class="annc">CHƯỚNG NGẠI VẬT CÓ {$states.key_length} CHỮ CÁI</div>
        <img src="data:image/webp;base64, {$states.image}" class="picture" alt="" />
    </div>
</div>

<style>
    .box {
        padding: 40px;
    }

    .annc {
        width: 100%;
        height: 60px;
        background-color: var(--accent);
        border-radius: var(--radius-1);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-s);
        font-weight: bold;
    }

    .code {
        font-family: var(--font-monospace);
    }

    .top {
        display: flex;
        flex-direction: row;
        gap: 60px;
        transform: translateY(-1.5rem);
    }

    .qbox {
        width: 40vw;
        height: 100%;
        min-height: 12rem;
        display: flex;
        justify-content: space-between;
        flex-direction: column;
    }

    .picontainer {
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: max-content;
        width: 40vw;
    }

    .timerbar {
        margin-top: 1rem;
        margin-bottom: -15px;
    }

    .picture {
        object-fit: cover;
        box-shadow: 7px 10px 33px 3px #00000040;
        height: 100%;
        border: solid 1px var(--border-color);
        border-radius: var(--radius-1);
        overflow: hidden;
    }

    .left {
        display: flex;
        flex-direction: column;
        gap: 60px;
    }

    .inp {
        width: 100%;
    }

    .up {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .answergroup {
        color: var(--text-2);
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;

        margin-bottom: 10px;
    }

    .ptag {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: inherit;
        height: 60px;
        transform: translateY(-4.5rem);
    }
</style>
