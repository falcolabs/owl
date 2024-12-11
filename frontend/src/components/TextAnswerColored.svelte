<script lang="ts">
    import PillTag from "./PillTag.svelte";

    export let name: string;
    export let time: number;
    export let content: string;
    export let verdict: boolean | null;
</script>

<div class="container">
    <div class="nametag">
        <PillTag text={name} />
    </div>
    <div class="answerbox box" class:wrong={!verdict && verdict !== null}>
        {#if content != ""}
            <p class="prompt">{content.toUpperCase()}</p>
        {:else}
            <p class="prompt">&nbsp</p>
        {/if}
        <span class="time">{time.toFixed(2).padStart(5, "0")}</span>
    </div>
</div>

<style>
    .box.wrong {
        background: #8a0f57;
    }

    .time {
        /* position: absolute; */
        font-size: var(--font-small);
        font-weight: bold;
        transform: translateY(-20px);
        font-family: var(--font-monospace);
    }

    .answerbox {
        width: 40vw;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 15px;
        padding-left: 25px;
        padding-top: 15px;
        padding-right: 25px;
        border-radius: var(--radius-1);
        background: #376b32;
    }

    .answerbox p {
        margin-top: 30px;
    }

    .nametag {
        transform: translateY(-40px) translateX(-20px);
    }
</style>
