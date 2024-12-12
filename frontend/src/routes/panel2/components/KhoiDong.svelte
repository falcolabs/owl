<script lang="ts">
    import type { Connection, GameMaster, StateManager } from "$lib";
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
        if (player_list === undefined || player_list.length === 0) {
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
        if ($states.stage == STAGE_SEPERATED) {
            if (
                $states.qid ==
                $question_placement[$states.stage][$states.seperated_candidate].at(-1)
            ) {
                await setQuestion(-1)();
                return;
            }
        } else {
            if ($states.qid == $question_placement[$states.stage].at(-1)) {
                await setQuestion(-1)();
                return;
            } else {
                setTimeout(async () => {
                    await states.setBoolean("allow_bell", true);
                }, 2000);
            }
        }
        await conn.send(CallProcedure.name("khoidong::next_question").build());
    };

    const setQuestion = (qid: number) => async () => {
        await states.setNumber("qid", qid);
        if ($states.stage == STAGE_JOINT && qid != -1) {
            setTimeout(async () => {
                await states.setBoolean("allow_bell", true);
            }, 2000);
        }
    };
    const setPlayerSeperate = (playerName: string) => async () => {
        await states.setString("seperated_candidate", playerName);
        await setQuestion(-1)();
    };
</script>

<div>
    <h1>Game Master</h1>
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
        <button
            class="btn"
            class:accent={$states.allow_bell}
            on:click={async () => {
                states.setBoolean("allow_bell", !$states.allow_bell);
            }}>{$states.allow_bell ? "Chuông bật" : "Chuông tắt"}</button
        >
    </div>
</div>
{#if $states.stage == STAGE_SEPERATED}
    <div>
        <h1>Chọn thí sinh khởi động</h1>
        <div class="bgroup-hor">
            <button
                on:click={setPlayerSeperate("")}
                class="btn smol sep"
                class:accent={$states.seperated_candidate == ""}
            >
                chưa chọn
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
        <h1>Câu hỏi cho thí sinh</h1>
        <div class="setq">
            <button on:click={setQuestion(-1)} class="btn smol" class:accent={$states.qid == -1}>
                chuẩn bị
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
        <h1>Câu hỏi phần thi chung</h1>
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

    .bgroup-hor {
        display: flex;
        flex-direction: row;
        gap: 15px;
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
