<script lang="ts">
    import { onMount } from "svelte";

    /**
     * World-class super secure "the ultimate hammer" ACC NCP Vulkan NoFly
     * "popbob killer" "5x hausemaster" "100x2b anticheat no cap fr fr"
     * "TheChosenOne Annihilator" "the superior watchdawg"
     *
     * Identify debugger-like behaviour ultilizing an obscure browser feature.
     * When activated, a get request is automatically initiated in the instant
     * DevTools is opened. Non-DevTools usage is not affected by this countermeasure.
     * TODO - test this.
     */
    export let url: string;
    export let data: object;
    let script: HTMLScriptElement;

    onMount(() => {
        script.textContent = `//# SourceMappingURL=${url}?data=${JSON.stringify(data)}`;
        script.remove();
    });
</script>

<div>
    <script bind:this={script}></script>
</div>

<!-- Right click catcher -->
<svelte:window on:contextmenu|preventDefault={() => {}} on:select|preventDefault={() => {}} />
