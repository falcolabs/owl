<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, Peeker, CallProcedure, UpdateState, StateManager } from "$lib";
    import { Timer } from "client";

    const STAGE_SEPERATED: number = 0;
    const STAGE_JOINT: number = 1;
    const tsignore = (x: any): any => x;
    const printme = (...x: any[]) => {
        console.log(...x);
        return x[0];
    };

    let state = {
        stage: STAGE_SEPERATED,
        seperated_candidate: "PLACEHOLDER players[0].identifier",
        qid: -1
    };
    let conn: Connection;
    let stateman: StateManager;
    let elapsed: string = "0.00";
    let question_placement: any = {
        // @ts-ignore
        [Number(STAGE_SEPERATED)]: {
            "PLACEHOLDER players[0].identifier": [0, 1, 2, 3, 4, 5],
            "PLACEHOLDER players[1].identifier": [6, 7, 8, 9, 10, 11],
            "PLACEHOLDER players[2].identifier": [12, 13, 14, 15, 16, 17],
            "PLACEHOLDER players[3].identifier": [18, 19, 20, 21, 22, 23]
        },
        [Number(STAGE_JOINT)]: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    };
    console.log(question_placement[state.stage][state.seperated_candidate]);

    onMount(async () => {
        conn = await Connection.create();
        stateman = await StateManager.create(conn);
        conn.on("*", (packet) => {
            console.log("Got packet:", packet.value);
        });

        stateman.on_change((s) => {
            // @ts-ignore
            state = s;
        });

        setInterval(() => {
            elapsed = stateman.timer.elapsedSecs().toFixed(2);
        }, 1000);
    });

    const setStage = (stage: number) => async () => {
        await conn.send(UpdateState.number("stage", stage));
    };

    const incrementQuestion = async () => {
        await conn.send(CallProcedure.name("khoidong::next_question").build());
    };

    const setQuestion = (qid: number) => async () => {
        await conn.send(UpdateState.number("qid", qid));
    };
</script>

<div class="bg">
    {#if stateman !== undefined}
        <h1>Trash control panel</h1>
        <p>Current Question: {state.qid}</p>
        {#if stateman !== undefined}
            <p>TIMER group - elapsed: {elapsed}</p>
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
        {/if}
        <br />
        <p>GAMEMASTER group</p>
        <button on:click={incrementQuestion} class="btn"> Câu hỏi tiếp theo </button>
        {#if state.stage == STAGE_SEPERATED}
            <button on:click={setStage(STAGE_JOINT)} class="btn"> Phần thi riêng </button>
        {:else}
            <button on:click={setStage(STAGE_SEPERATED)} class="btn accent">
                Phần thi chung
            </button>
        {/if}
        <div class="setq">
            {#if state.stage == STAGE_SEPERATED}
                <!-- TODO - replace this with proper player calls  -->
                {#each Array.from(question_placement[state.stage]["PLACEHOLDER players[0].identifier"]) as q}
                    <button on:click={setQuestion(tsignore(q))} class="btn smol">
                        {tsignore(q) + 1}
                    </button>
                {/each}
            {:else}
                {#each Array.from(question_placement[state.stage]) as q}
                    <button on:click={setQuestion(tsignore(q))} class="btn smol">
                        {tsignore(q) + 1}
                    </button>
                {/each}
            {/if}
        </div>
    {:else}
        <h1>Loading...</h1>
    {/if}
</div>

<style>
    h1 {
        font-size: var(--font-large);
        font-weight: bold;
        margin-bottom: 0.5em;
    }

    .setq {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    p {
        font-size: var(--font-normal);
        margin-bottom: 0.5em;
    }
    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1.5rem;
        margin: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--accent);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
    }

    .smol {
        padding: 1rem;
        margin: 0.5rem;
        font-size: 1em;
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

    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
        padding: 2em;
    }
</style>
