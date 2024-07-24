<script lang="ts">
    import PillTag from "../../../components/PillTag.svelte";
    import ScoreBar from "../../../components/ScoreBar.svelte";
    import TitleBar from "../../../components/TitleBar.svelte";

    const current_question = {
        prompt: "Nguyên liệu để sản xuất bromine (Br) trong công nghiệp là gì?"
    };
</script>

<title>Khởi động - Đường đua xanh</title>
<div class="bg">
    <TitleBar activity="Khởi động" />
    <div class="center-box">
        <div class="box">
            <PillTag text="Câu 1" />
            <p class="prompt">{current_question.prompt}</p>
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
        transform: translateY(12rem);
    }
</style>
