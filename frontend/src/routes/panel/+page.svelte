<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, Peeker, CallProcedure, Push, GameMaster, StateManager } from "$lib";
    import { Timer, type Player } from "client";
    import { readable, writable, get, type Writable, type Readable } from "svelte/store";
    import ScoreBar from "../../components/ScoreBar.svelte";

    const STAGE_SEPERATED: number = 0;
    const STAGE_JOINT: number = 1;
    const tsignore = (x: any): any => x;
    const printme = (x: any) => {
        console.log(x);
        return x;
    };

    let conn: Connection;
    let gm: GameMaster;
    // @ts-ignore
    let timer: Writable<Timer> = writable({ elapsedSecs: () => 6.9 });
    let players: Readable<Map<string, Player>> = readable(new Map());
    let elapsed = "0.00";
    $: elapsed = $timer.elapsedSecs().toFixed(2);
    // @ts-ignore
    let states: StateManager = readable({
        stage: STAGE_SEPERATED,
        seperated_candidate: "PLACEHOLDER players[0].identifier",
        qid: -1
    });
    let question_placement: Writable<any> = writable({
        [Number(STAGE_SEPERATED)]: {
            "PLACEHOLDER players[0].identifier": [0, 1, 2, 3, 4, 5],
            "PLACEHOLDER players[1].identifier": [6, 7, 8, 9, 10, 11],
            "PLACEHOLDER players[2].identifier": [12, 13, 14, 15, 16, 17],
            "PLACEHOLDER players[3].identifier": [18, 19, 20, 21, 22, 23]
        },
        [Number(STAGE_JOINT)]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    });

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        players.subscribe((p) => {
            let player_list = Array.from(p.values());
            if (player_list.length === 0) {
                return;
            }
            $question_placement = {
                // @ts-ignore
                [Number(STAGE_SEPERATED)]: {
                    [player_list[0].identifier]: [0, 1, 2, 3, 4, 5],
                    [player_list[1].identifier]: [6, 7, 8, 9, 10, 11],
                    [player_list[2].identifier]: [12, 13, 14, 15, 16, 17],
                    [player_list[3].identifier]: [18, 19, 20, 21, 22, 23]
                },
                [Number(STAGE_JOINT)]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            };
        });
        timer = states.timerStore;
    });

    const setStage = (stage: number) => async () => await states.setNumber("stage", stage);

    const incrementQuestion = async () => {
        await conn.send(CallProcedure.name("khoidong::next_question").build());
    };

    const setQuestion = (qid: number) => async () => await states.setNumber("qid", qid);
    const setPlayerSeperate = (playerName: string) => async () => {
        await states.setString("seperated_candidate", playerName);
    };
</script>

<div class="bg">
    <div class="container">
        {#if gm !== undefined}
            <h1>Trash control panel</h1>
            <ScoreBar gamemaster={gm} />
            <div>
                <p>Current Question: <span class="code">&nbsp{$states.qid + 1}</span></p>
                <p>Prompt: <span class="code">&nbsp{$states.current_question_content}</span></p>
            </div>
            <div>
                <p>Time Elapsed: <span class="code">&nbsp{elapsed}</span></p>
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
            <div>
                <p>Game Master Controls</p>
                <div class="bgroup-hor">
                    <button on:click={incrementQuestion} class="btn"> Câu hỏi tiếp theo </button>
                    {#if $states.stage == STAGE_SEPERATED}
                        <button on:click={setStage(STAGE_JOINT)} class="btn">
                            Phần thi riêng
                        </button>
                    {:else}
                        <button on:click={setStage(STAGE_SEPERATED)} class="btn accent">
                            Phần thi chung
                        </button>
                    {/if}
                </div>
            </div>
            <div>
                <p>Chọn thí sinh khởi động</p>
                <div class="bgroup-hor">
                    {#if $states.stage == STAGE_SEPERATED}
                        <button on:click={setPlayerSeperate("")} class="btn smol sep">
                            unset
                        </button>
                        {#each $players as [ident, p]}
                            <button on:click={setPlayerSeperate(ident)} class="btn smol">
                                {p.name}
                            </button>
                        {/each}
                    {/if}
                </div>
            </div>
            <div>
                <p>Câu hỏi cho thí sinh</p>
                <div class="setq">
                    <button on:click={setQuestion(-1)} class="btn smol"> prepare </button>
                    {#if $states.stage == STAGE_SEPERATED && $question_placement[$states.stage][$states.seperated_candidate] !== undefined}
                        {#each $question_placement[$states.stage][$states.seperated_candidate] as q}
                            <button on:click={setQuestion(tsignore(q))} class="btn smol code">
                                {tsignore(q) + 1}
                            </button>
                        {/each}
                    {:else if $states.stage == STAGE_JOINT}
                        {#each printme($question_placement[$states.stage]) as q}
                            <button on:click={setQuestion(tsignore(q))} class="btn smol code">
                                {tsignore(q) + 1}
                            </button>
                        {/each}
                    {:else}
                        <p>
                            {$states.stage == STAGE_SEPERATED
                                ? "No candidate selected."
                                : "IMPOSSIBLE SITUATION!!!"}
                        </p>
                    {/if}
                </div>
            </div>
        {:else}
            <h1>Loading...</h1>
        {/if}
    </div>
</div>

<style>
    h1 {
        font-size: var(--font-large);
        font-weight: bold;
        width: fit-content;
    }

    .setq {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    p {
        font-size: var(--font-normal);
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

    .smol {
        padding: 15px;
        margin: 0.5rem;
        margin-left: 0;
        font-size: 1em;
        border-radius: 9px;
        border: none;
    }

    .accent {
        background-color: var(--border-color);
    }

    .btn:hover {
        filter: brightness(90%);
    }

    .btn:active {
        filter: brightness(80%);
    }

    .bgroup-hor {
        display: flex;
        flex-direction: row;
    }

    .container {
        display: flex;
        flex-direction: column;
        gap: 25px;
        width: fit-content;
    }

    .sep {
        margin-right: 2rem;
    }

    .code {
        font-family: var(--font-monospace);
    }

    .bg {
        position: fixed;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: var(--bg-dark-1);
        padding: 2em;
    }
</style>
