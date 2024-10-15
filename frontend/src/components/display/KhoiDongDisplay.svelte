<script lang="ts">
    import { onMount } from "svelte";
    import PillTag from "../PillTag.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import TitleBar from "../TitleBar.svelte";
    import Load from "../Load.svelte";

    import { goto } from "$app/navigation";
    import { Peeker, Connection, GameMaster, type AcceptableValue, PlayerManager } from "$lib";
    import { readable, type Readable } from "svelte/store";
    const STAGE_SEPERATED = 0;
    const STAGE_JOINT = 1;
    export let conn: Connection;
    export let gm: GameMaster;
    export let states: Readable<any> = readable({
        qid: -1,
        current_question_content: ""
    });
    export let players: PlayerManager;
</script>

<title>Khởi động - Đường đua xanh</title>
<div class="bg">
    <TitleBar activity="Khởi động" />
    <div class="center-box">
        <div class="box">
            {#if $states.qid > -1}
                <div class="qnum"><PillTag text="Câu {$states.qid + 1}" /></div>
                <p class="prompt">{$states.current_question_content}</p>
            {:else}
                <div class="qnum"><PillTag text="Chuẩn bị" /></div>
                <p class="prompt">Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.</p>
            {/if}
            <div class="sbar"><ScoreBar players={gm.players} {states} /></div>
        </div>
    </div>
</div>

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

    .box {
        padding: 3em 5em;
        margin-top: 50px;
        width: 60vw;
        height: 30vh;
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
</style>
