<script lang="ts">
    import { Peeker, Connection, GameMaster } from "$lib";
    import { onMount } from "svelte";
    import { readable, writable, type Readable } from "svelte/store";
    import Load from "../../../components/Load.svelte";
    import TitleBar from "../../../components/TitleBar.svelte";
    import VcnvMain from "../../../components/vcnv/VCNVMain.svelte";
    import VcnvShowAnswer from "../../../components/vcnv/VCNVShowAnswer.svelte";
    import ScoreBar from "../../../components/ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";

    let conn: Connection;
    let gm: GameMaster;
    let states: Readable<any> = readable({
        puzzle_data: [
            { status: "shown", content: "mrbeast", tag: "1" },
            { status: "shown", content: "trump", tag: "2" },
            { status: "shown", content: "ohio", tag: "3" },
            { status: "shown", content: "しかせんべい", tag: "4" }
        ],
        prompt: 'Đây là những lời nhận xét của Hoài Thanh - Hoài Chân về ai: "chỉ tiên sinh là người của hai thế kỷ. Tiên sinh sẽ đại biểu cho một lớp người để chứng giám công việc lớp người kế tiếp. Ở địa vị ấy còn có ai xứng đáng hơn tiên sinh"?',
        key_length: 69,
        image: "",
        show_key: false,
        answers: [
            { time: 29.5, name: "MrBeast", content: "IELT", verdict: null },
            { time: 1.3, name: "Joe Biden", content: "O-O-O", verdict: true },
            { time: 69.42, name: "Trump", content: "d4d5", verdict: false },
            { time: 2, name: "herobrine", content: "sasfsf", verdict: null }
        ]
    });
    let players: PlayerManager;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
    });
</script>

<title>Vượt chướng ngại vật - Đường đua xanh</title>
<div class="bg">
    <Load until={gm !== undefined && $states.__init}>
        <TitleBar activity="Vượt chướng ngại vật" />
        <div class="center-box">
            {#if $states.show_key}
                <div class="answers">
                    <VcnvShowAnswer {states} />
                </div>
            {:else}
                <div class="main">
                    <VcnvMain {states} />
                </div>
            {/if}
        </div>
        <div class="bottom"><ScoreBar {players} {states} /></div>
    </Load>
</div>

<style>

    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .center-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        flex-direction: column;
        transform: translateY(2rem);
    }

    .bottom {
        position: absolute;
        transform: translateY(-5rem);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
    }
</style>
