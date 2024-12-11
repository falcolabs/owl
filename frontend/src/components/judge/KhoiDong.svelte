<script lang="ts">
    import { CallProcedure, Connection, GameMaster, type StateManager } from "$lib";
    import { onMount } from "svelte";
    import { writable, readable, type Writable } from "svelte/store";

    const STAGE_SEPERATED: number = 0;
    const STAGE_JOINT: number = 1;
    // @ts-ignore
    export let states: StateManager;
    export let conn: Connection;
    export let gm: GameMaster;

    let question_placement: Writable<any> = writable({
        [Number(STAGE_SEPERATED)]: {
            "PLACEHOLDER players[0].identifier": [0, 1, 2, 3, 4, 5],
            "PLACEHOLDER players[1].identifier": [6, 7, 8, 9, 10, 11],
            "PLACEHOLDER players[2].identifier": [12, 13, 14, 15, 16, 17],
            "PLACEHOLDER players[3].identifier": [18, 19, 20, 21, 22, 23]
        },
        [Number(STAGE_JOINT)]: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    });

    const onKeyDown = async (ev: KeyboardEvent) => {
        if (ev.key === " ") {
            if ($states.qid != -1) {
                await incrementQuestion();
            } else {
                if ($states.stage == STAGE_SEPERATED) {
                    await setQuestion(
                        $question_placement[$states.stage][$states.seperated_candidate][0]
                    )();
                } else {
                    await setQuestion($question_placement[$states.stage][0])();
                }
            }
        }
        if ($states.stage == STAGE_SEPERATED) {
            if (ev.key === "+") {
                await gm.add_score($states.seperated_candidate, $states.plusminus.add[0]);
                await gm.sound.play("khoidong-correct");
            }
            if (ev.key === "-") {
                await gm.add_score($states.seperated_candidate, $states.plusminus.rem[0]);
                await gm.sound.play("khoidong-incorrect");
            }
        } else {
            if (ev.key === "+") {
                await gm.add_score($states.joint_bell, $states.plusminus.add[0]);
                await gm.sound.play("khoidong-correct");
            }
            if (ev.key === "-") {
                await gm.add_score($states.joint_bell, $states.plusminus.rem[0]);
                await gm.sound.play("khoidong-incorrect");
            }
        }
    };

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
</script>

<svelte:window on:keydown={onKeyDown} />
