<script lang="ts">
    import { Peeker, Connection, GameMaster, StateManager } from "$lib";
    import { readable, writable, type Readable } from "svelte/store";
    import Load from "../Load.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";
    import VcnvMainReduced from "../vcnv/VCNVMainReduced.svelte";
    import ShowAnswerColored from "../ShowAnswerColored.svelte";

    export let conn: Connection;
    export let gm: GameMaster;
    // @ts-ignore
    export let states: StateManager = readable({
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
    export let players: PlayerManager;
</script>

<title>Vượt chướng ngại vật - Đường đua xanh</title>
<div class="bg">
    <Load until={$states.selected !== undefined}>
        <div class="center-box">
            <div class="main">
                <VcnvMainReduced {states} />
            </div>
            <div class="answers">
                <ShowAnswerColored {states} {players} />
            </div>
        </div>
        <div class="bottom"><ScoreBar {states} /></div>
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
        flex-direction: row;
        gap: 50px;
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
