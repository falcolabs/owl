<script lang="ts">
    import { Peeker, Connection, GameMaster } from "$lib";
    import { onMount } from "svelte";
    import { readable, writable, type Readable } from "svelte/store";
    import Load from "../../../components/Load.svelte";
    import TitleBar from "../../../components/TitleBar.svelte";
    import DATA from "../../../p2b64.b64?raw";
    import VcnvMain from "../../../components/VCNVMain.svelte";
    import VcnvShowAnswer from "../../../components/VCNVShowAnswer.svelte";

    let conn: Connection;
    let gm: GameMaster;
    let states: Readable<any> = readable({
        current_key: [
            {status: "shown", content: "mrbeast", tag: "1"},
            {status: "shown", content: "trump", tag: "2"},
            {status: "shown", content: "ohio", tag: "3"},
            {status: "shown", content: "しかせんべい", tag: "4"}
        ],
        prompt: "Đây là những lời nhận xét của Hoài Thanh - Hoài Chân về ai: \"chỉ tiên sinh là người của hai thế kỷ. Tiên sinh sẽ đại biểu cho một lớp người để chứng giám công việc lớp người kế tiếp. Ở địa vị ấy còn có ai xứng đáng hơn tiên sinh\"?",
        key_length: 69,
        image: DATA,
        show_key: false,
        answers: [
            {time: 29.5,name: "MrBeast", content: "IELT", verdict: null},
            {time: 1.3,name: "Joe Biden", content: "O-O-O", verdict: true},
            {time: 69.42,name: "Trump", content: "d4d5", verdict: false},
            {time: 2,name: "herobrine", content: "sasfsf", verdict: null}
        ]
    });

    // onMount(async () => {
    //     conn = await Connection.create();
    //     gm = await GameMaster.create(conn);
    //     states = gm.states;
    // });
</script>

<title>Vượt chướng ngại vật - Đường đua xanh</title>
<div class="bg">
    <!-- <Load until={gm !== undefined}> -->
    <TitleBar activity="Vượt chướng ngại vật" />
    <div class="center-box">
        <div class="main">
            <VcnvMain {states} />
        </div>
        <div class="answers hidden">
            <VcnvShowAnswer {states} />
        </div>
        <div class="bottom">scoreboard</div>
    </div>
    <!-- </Load> -->
</div>

<style>
    .hidden {
        display: none;
    }
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
        height: 100%;
        flex-direction: column;
        transform: translateY(40px);
    }

    .bottom {
        margin-top: 30px;
    }

</style>
