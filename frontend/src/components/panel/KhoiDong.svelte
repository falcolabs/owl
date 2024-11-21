<script lang="ts">
    import type { Connection, StateManager } from "$lib";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    import { CallProcedure } from "$lib";
    import type { Timer, Player } from "client";
    import { onMount } from "svelte";

    const tsignore = (x: any): any => x;
    const printme = (x: any) => {
        console.log(x);
        return x;
    };

    const STAGE_SEPERATED: number = 0;
    const STAGE_JOINT: number = 1;
    // @ts-ignore
    export let states: StateManager = readable({
        stage: STAGE_SEPERATED,
        seperated_candidate: "PLACEHOLDER players[0].identifier",
        qid: -1
    });
    export let conn: Connection;
    export let players: Readable<Map<string, Player>>;

    let question_placement: Writable<any> = writable({
        [Number(STAGE_SEPERATED)]: {
            "PLACEHOLDER players[0].identifier": [0, 1, 2, 3, 4, 5],
            "PLACEHOLDER players[1].identifier": [6, 7, 8, 9, 10, 11],
            "PLACEHOLDER players[2].identifier": [12, 13, 14, 15, 16, 17],
            "PLACEHOLDER players[3].identifier": [18, 19, 20, 21, 22, 23]
        },
        [Number(STAGE_JOINT)]: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    });

    onMount(async () => {
        let player_list = $states.engine_players;
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
            [Number(STAGE_JOINT)]: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        };
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

<div>
    <p class="code">Question #{$states.qid + 1}. {$states.current_question_content}</p>
</div>

<div>
    <p>Game Master Controls</p>
    <div class="bgroup-hor">
        <button
            on:click={$states.qid != -1
                ? incrementQuestion
                : async () => {
                      if ($states.stage == STAGE_SEPERATED) {
                          await setQuestion(
                              $question_placement[$states.stage][$states.seperated_candidate][0]
                          )();
                      } else {
                          await setQuestion($question_placement[$states.stage][0])();
                      }
                  }}
            class="btn"
        >
            Câu hỏi tiếp theo
        </button>
        <button
            class="btn"
            on:click={async () => {
                if ($states.stage == STAGE_JOINT) {
                    await states.setString("joint_bell", "");
                    await states.setArray("highlighted", []);
                }
            }}
        >
            Xóa chuông
        </button>
        {#if $states.stage == STAGE_SEPERATED}
            <button on:click={setStage(STAGE_JOINT)} class="btn"> Phần thi riêng </button>
        {:else}
            <button on:click={setStage(STAGE_SEPERATED)} class="btn accent">
                Phần thi chung
            </button>
        {/if}
    </div>
</div>
{#if $states.stage == STAGE_SEPERATED}
    <div>
        <p>Chọn thí sinh khởi động</p>
        <div class="bgroup-hor">
            <button
                on:click={setPlayerSeperate("")}
                class="btn smol sep"
                class:accent={$states.seperated_candidate == ""}
            >
                unset
            </button>
            {#each $players as [ident, p]}
                <button
                    on:click={setPlayerSeperate(ident)}
                    class="btn smol"
                    class:accent={ident == $states.seperated_candidate}
                >
                    {p.name}
                </button>
            {/each}
        </div>
    </div>
    <div>
        <p>Câu hỏi cho thí sinh</p>
        <div class="setq">
            <button on:click={setQuestion(-1)} class="btn smol" class:accent={$states.qid == -1}>
                prepare
            </button>
            {#if $question_placement[$states.stage][$states.seperated_candidate] !== undefined}
                {#each $question_placement[$states.stage][$states.seperated_candidate] as q}
                    <button
                        on:click={setQuestion(tsignore(q))}
                        class="btn smol code eqsize"
                        class:accent={q == $states.qid}
                    >
                        {tsignore(q) + 1}
                    </button>
                {/each}
            {/if}
        </div>
    </div>
{:else if $states.stage == STAGE_JOINT}
    <div>
        <p>Câu hỏi phần thi chung</p>
        <div class="setq">
            <button on:click={setQuestion(-1)} class="btn smol" class:accent={$states.qid == -1}>
                prepare
            </button>
            {#each $question_placement[$states.stage] as q}
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
{/if}

<style>
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
