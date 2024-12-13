<script lang="ts">
    import TitleBar from "../TitleBar.svelte";
    import PackageChooser from "../vedich/PackageChooser.svelte";
    import { writable } from "svelte/store";
    import PillTag from "../PillTag.svelte";
    import Load from "../Load.svelte";
    import { scoreOf } from "$lib/globals";
    import { Connection, GameMaster, PlayerManager, StateManager } from "$lib";
    import ScoreBar from "../ScoreBar.svelte";
    import TimerBar from "../TimerBar.svelte";
    import { CallProcedure } from "$lib";
    const STAGE_CHOOSE: number = 0;
    const STAGE_COMPETE: number = 1;

    export let conn: Connection;
    export let gm: GameMaster;
    // @ts-ignore
    export let states: StateManager = writable({
        package: {
            mrbeast: [20, 30, 20],
            trump: [20, 30, 20],
            qliem: [20, 30, 20],
            potrait: [20, 30, 20]
        },
        current_player_username: "mrbeast",
        prompt: "",
        stage: STAGE_COMPETE,
        qid: -1
    });
    export let players: PlayerManager;
</script>

<title>Về đích - Đường đua xanh</title>
<div class="bg">
    <Load until={gm !== undefined && $states.package !== undefined}>
        <div class="center-box">
            {#if $states.stage == STAGE_CHOOSE}
                {#if $states.current_player_username !== ""}
                    <div class="vertical">
                        <PackageChooser {states} />
                    </div>
                {/if}
            {:else}
                <div class="box">
                    {#if $states.qid > -1}
                        <div class="qnum">
                            <Load until={$states.placement[$states.current_player_username] !== undefined}>
                                <PillTag
                                    text={`Câu ${$states.placement[$states.current_player_username].indexOf($states.qid) + 1}` +
                                        ($states.hope_stars.includes($states.qid) ? " ☆" : "") +
                                        " · " +
                                        `${scoreOf[$states.qid]}` +
                                        "đ"}
                                />
                            </Load>
                        </div>
                        <p class="prompt">{$states.prompt}</p>
                    {:else}
                        <div class="qnum"><PillTag text="Chuẩn bị" /></div>
                        <p class="prompt">
                            Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.
                        </p>
                    {/if}
                </div>
                <div class="timerbar"><TimerBar {states} /></div>
            {/if}
        </div>
        <div class="bottom">
            <button
                class="btn answercnv"
                class:activated={$states.highlighted.includes(gm.username)}
                on:click={async () => {
                    await conn.send(
                        CallProcedure.name("vedich::bell")
                            .string("token", gm.authToken)
                            .string("clientTime", `${Date.now()}`)
                            .build()
                    );
                }}>Chuông trả lời</button
            >
            <ScoreBar {states} />
        </div>
    </Load>
</div>

<style>
    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--bg-dark-2);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: fit-content;
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

    .bottom {
        position: fixed;
        left: 0px;
        bottom: 1rem;
        max-width: 80%;
        width: 80%;
        margin: 0;
        padding-left: 10vw;
        padding-right: 10vw;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .timerbar {
        width: 70vw;
        margin-top: 15px;
    }

    .qnum {
        position: absolute;
        width: 60vw;
        transform: translateY(-7rem);
        display: flex;
        justify-content: center;
    }

    .box {
        padding: 3em 5em;
        margin-top: 50px;
        width: 60vw;
        height: 40vh;
        text-align: justify;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }
</style>
