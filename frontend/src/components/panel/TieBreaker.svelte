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

    let question_placement: Writable<any> = writable([69, 70, 71]);

    onMount(async () => {
        let player_list = $states.engine_players;
        if (player_list.length === 0) {
            return;
        }
    });

    const incrementQuestion = async () => {
        if ($states.qid == $question_placement.at(-1)) {
            await setQuestion(-1)();
            return;
        }
        await conn.send(CallProcedure.name("tiebreaker::next_question").build());
    };

    const setQuestion = (qid: number) => async () => await states.setNumber("qid", qid);
</script>

<div>
    <p class="code">Question #{$states.qid + 1}. {$states.current_question_content}</p>
</div>

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
</style>
