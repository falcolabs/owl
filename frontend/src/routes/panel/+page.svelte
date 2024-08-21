<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, Peeker, CallProcedure, UpdateState, StateManager } from "$lib";
    import { Timer } from "client";
    const STAGE_SEPERATED = 0;
    const STAGE_JOINT = 1;
    let stage: 0 | 1;
    let qid: number;
    let conn: Connection;
    let stateman: StateManager;
    let elapsed: string = "0.00";
    const question_placement = {
        STAGE_SEPERATED: [
            [0, 1, 2, 3, 4, 5],
            [6, 7, 8, 9, 10, 11],
            [12, 13, 14, 15, 16, 17],
            [18, 19, 20, 21, 22, 23]
        ],
        STAGE_JOINT: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    };

    onMount(async () => {
        conn = await Connection.create();
        stateman = await StateManager.create(conn);
        conn.on("*", (packet) => {
            console.log("Got packet:", packet.value);
        });
        // await conn.send(Peeker.Query.stateList());
        stateman.on_value("qid", (q) => {
            // @ts-ignore
            qid = q;
        });

        stateman.on_value("stage", (q) => {
            // @ts-ignore
            stage = q;
        });

        setInterval(() => {
            elapsed = stateman.timer.elapsedSecs().toFixed(2);
        }, 1000);
    });

    const setStage = (stage: 0 | 1) => async () => {
        await conn.send(UpdateState.number("stage", stage));
    };

    const incrementQuestion = async () => {
        await conn.send(CallProcedure.name("khoidong::next_question").build());
    };
</script>

<div class="bg">
    <h1>Trash control panel</h1>
    <p>Current Question: {qid}</p>
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
    {#if stage == STAGE_SEPERATED}
        <button on:click={setStage(STAGE_JOINT)} class="btn"> Phần thi riêng </button>
    {:else}
        <button on:click={setStage(STAGE_SEPERATED)} class="btn accent"> Phần thi chung </button>
    {/if}
</div>

<style>
    h1 {
        font-size: var(--font-large);
        font-weight: bold;
        margin-bottom: 0.5em;
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
