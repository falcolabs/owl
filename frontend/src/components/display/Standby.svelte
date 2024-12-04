<script lang="ts">
    import { SHOW_NAME, ORG_NAME, SUBTEXT } from "$lib";
</script>

<div class="bg">
    <img alt="" src="/bg.jpg" />
    <!-- <div></div>
    <div class="titlegroup">
        <h2 class="caps">{ORG_NAME}</h2>
        <h1>
            {SHOW_NAME}
        </h1>
        <h2 class="caps subtext">{SUBTEXT}</h2>
    </div>
    <p class="cpy">Ⓒ 2024 {ORG_NAME}. Đây là phần mềm nguồn mở, phát hành theo giấy phép GPL3.</p> -->
</div>

<style>
    img {
        width: 100%;
        height: 100%;
    }
    .bg {
        width: 100%;
        height: 100vh;
        background: var(--bg-gradient);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        overflow: hidden;
    }
</style>
