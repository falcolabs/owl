<script lang="ts">
    import { onMount } from "svelte";
    import PillTag from "../../../components/PillTag.svelte";
    import ScoreBar from "../../../components/ScoreBar.svelte";
    import TitleBar from "../../../components/TitleBar.svelte";
    import { goto } from "$app/navigation";
    import { Peeker, Connection, StateManager, type AcceptableValue } from "$lib";
    const STAGE_SEPERATED = 0;
    const STAGE_JOINT = 1;
    let conn: Connection;
    let stateman: StateManager;
    let state = {
        qid: -1,
        current_question_content: ""
    };
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
        // @ts-ignore
        stateman.on_change((s) => (state = s));
        
    });
</script>

<title>Khởi động - Đường đua xanh</title>
<div class="bg">
    <TitleBar activity="Khởi động" />
    <div class="center-box">
        <div class="box">
            {#if state.qid > -1}
                <PillTag text="Câu {state.qid}" />
                <p class="prompt">{state.current_question_content}</p>
            {:else}
                <PillTag text="Chuẩn bị" />
                <p class="prompt">Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.</p>
            {/if}
            <div class="sbar"><ScoreBar /></div>
        </div>
    </div>
</div>

<style>
    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
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
