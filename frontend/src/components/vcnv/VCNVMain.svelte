<script lang="ts">
    import VcnvLine from "./VCNVLine.svelte";
    import PillTag from "./PillTag.svelte";
    import type { StateManager } from "$lib";
    import type { Readable } from "svelte/store";
    export let states: Readable<any>;
</script>

<div class="top">
    <div class="left">
        <div class="up box">
            {#each $states.puzzle_data as { content, status, tag }}
                <VcnvLine {content} {status} {tag}></VcnvLine>
            {/each}
        </div>
        <div class="qbox box">
            <div class="ptag"><PillTag text="Hàng 1" /></div>
            <p class="prompt">{$states.prompt}</p>
            <div class="timerbar">timerbar</div>
        </div>
    </div>
    <div class="picontainer">
        <div class="annc">CHƯỚNG NGẠI VẬT CÓ {$states.key_length} CHỮ CÁI</div>
        <img src="data:image/png;base64, {$states.image}" class="picture" alt="" />
    </div>
</div>

<style>
    .box {
        padding: 40px;
    }

    .annc {
        height: 60px;
        background-color: var(--accent);
        border-radius: var(--radius-1);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-s);
        font-weight: bold;
    }

    .top {
        display: flex;
        flex-direction: row;
        gap: 60px;
    }

    .qbox {
        width: 40vw;
        height: 100%;
    }

    .picontainer {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .timerbar {
        margin-top: 2rem;
        margin-bottom: -15px;
    }

    .picture {
        box-shadow: 7px 10px 33px 3px #00000040;
        height: 100%;
        border-radius: var(--radius-1);
        overflow: hidden;
    }

    .left {
        display: flex;
        flex-direction: column;
        gap: 60px;
    }

    .up {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .ptag {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: inherit;
        height: 60px;
        transform: translateY(-4.5rem);
    }
</style>
