<script lang="ts">
    import PillTag from "../PillTag.svelte";
    import ScoreBar from "../ScoreBar.svelte";

    import { CallProcedure, Connection, GameMaster, PlayerManager, StateManager } from "$lib";
    import TimerBar from "../TimerBar.svelte";
    export let conn: Connection;
    export let gm: GameMaster;
    export let states: StateManager;
    export let players: PlayerManager;

    const onKeyDown = async (_) => {
        await conn.send(
            CallProcedure.name("tiebreaker::ring_bell").string("token", gm.authToken!).build()
        );
    };
</script>

<title>Câu hỏi phụ - Đường đua xanh</title>
<div class="bg">
    <div class="center-box">
        <div class="container">
            <div class="box">
                {#if $states.qid > -1}
                    <div class="qnum"><PillTag text="Câu {$states.display_qid}" /></div>
                    <p class="prompt">{$states.current_question_content}</p>
                {:else}
                    <div class="qnum"><PillTag text="Chuẩn bị" /></div>
                    <p class="prompt">Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.</p>
                {/if}
                <div class="sbar"><ScoreBar {states} /></div>
            </div>
            <div class="timerbar">
                <TimerBar {states} />
            </div>
        </div>
        <h1 class="bellnotify">Click chuột hay bấm bất kỳ phím nào để rung chuông</h1>
    </div>
</div>
<svelte:window on:keydown|preventDefault={onKeyDown} on:mousedown={onKeyDown} />


<style>
    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
        display: flex;
    }

    .qnum {
        position: absolute;
        width: 60vw;
        transform: translateY(-7rem);
        display: flex;
        justify-content: center;
    }

    .container {
        margin-top: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-items: center;
        gap: 15px;
    }

    .timerbar {
        width: 95%;
    }

    .box {
        width: 60vw;
        height: 40vh;
        padding: 3em 5em;
        text-align: justify;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .center-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100%;
        flex-direction: column;
    }

    .sbar {
        transform: translateY(3rem);
    }

    .bellnotify {
        transform: translateY(4rem);
        color: var(--border-color);
        font-size: 2rem;
        font-weight: bold;
    }
</style>
