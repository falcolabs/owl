<script lang="ts">
    import { SHOW_NAME, ORG_NAME } from "$lib";
</script>

<div class="bg">
    <div></div>
    <div class="titlegroup">
        <h2 class="caps">{ORG_NAME}</h2>
        <h1>
            {SHOW_NAME}
        </h1>
    </div>
    <p class="cpy">Ⓒ 2024 {ORG_NAME}. Đây là phần mềm nguồn mở, phát hành theo giấy phép GPL3.</p>
</div>

<style>
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

    .titlegroup {
        display: flex;
        flex-direction: column;
        justify-self: center;
        align-items: center;
    }

    .cpy {
        font-size: 16px;
        text-align: center;
        color: #888ebf;
        margin-bottom: 15px;
        width: 540px;
    }

    .caps {
        text-transform: uppercase;
        margin-bottom: 0.5em;
    }

    h2 {
        font-size: 1.5rem;
        color: var(--text-2);
        font-weight: bold;
    }
    h1 {
        font-size: 4rem;
        color: var(--text);
        font-weight: bold;
    }
</style>
