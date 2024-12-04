<script lang="ts">
    import type { Connection, StateManager } from "$lib";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    import { CallProcedure } from "$lib";
    import type { Timer, Player } from "client";
    import { onMount } from "svelte";

    const tsignore = (x: any): any => x;

    // @ts-ignore
    export let states: StateManager = readable({});
    export let conn: Connection;
    export let players: Readable<Map<string, Player>>;

    let question_placement: Writable<any> = writable([70, 71, 72]);

    const incrementQuestion = async () => {
        if ($states.qid == $question_placement.at(-1)) {
            await setQuestion(-1)();
            return;
        }
        setTimeout(async () => {
            await states.setBoolean("allow_bell", true);
        }, 2000);
        await conn.send(CallProcedure.name("tiebreaker::next_question").build());
    };

    const setQuestion = (qid: number) => async () => {
        await states.setNumber("qid", qid);
        if (qid != -1) {
            setTimeout(async () => {
                await states.setBoolean("allow_bell", true);
            }, 2000);
        }
    };
</script>

<div>
    <h1>Game Master Controls</h1>
    <div class="bgroup-hor">
        <button
            on:click={$states.qid != -1
                ? incrementQuestion
                : async () => {
                      await setQuestion($question_placement[0])();
                  }}
            class="btn"
        >
            Câu hỏi tiếp theo
        </button>
        <button
            class="btn"
            on:click={async () => {
                await states.setString("joint_bell", "");
                await states.setArray("highlighted", []);
            }}
        >
            Xóa chuông
        </button>
        <button
            class="btn"
            class:accent={$states.allow_bell}
            on:click={async () => {
                states.setBoolean("allow_bell", !$states.allow_bell);
            }}>{$states.allow_bell ? "Chuông bật" : "Chuông tắt"}</button
        >
    </div>
</div>

<div>
    <h1>Câu hỏi phần thi chung</h1>
    <div class="setq">
        <button on:click={setQuestion(-1)} class="btn smol" class:accent={$states.qid == -1}>
            prepare
        </button>
        {#each $question_placement as q}
            <button
                on:click={setQuestion(tsignore(q))}
                class="btn smol code eqsize"
                class:accent={q == $states.qid}
            >
                {tsignore(q) + 1}
            </button>
        {/each}
    </div>
</div>
<div class="qdisplay">
    <p>Câu {$states.qid + 1}. {$states.prompt}</p>
    <p style="font-weight: bold;">{$states.key}</p>
</div>

<style>
    .setq {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    h1 {
        font-weight: bold;
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
        background-color: var(--accent);
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
    .sep {
        margin-right: 2rem;
    }

    .code {
        font-family: var(--font-monospace);
    }

    .eqsize {
        display: flex;
        width: 70px;
        height: auto;
        align-items: center;
        justify-content: center;
    }

    .qdisplay {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
