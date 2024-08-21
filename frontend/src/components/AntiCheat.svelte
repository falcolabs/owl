<script lang="ts">
    import { onMount } from "svelte";

    /**
     * World-class super secure "the ultimate hammer" ACC NCP Vulkan NoFly
     * "popbob killer" "5x hausemaster" "100x2b anticheat no cap fr fr"
     *
     * Detects debugger using an old feature named SourceMappingURL.
     * When the browser devtools is open, it automatically sends a get request
     * to the specified URL. This does not affect non-devtools usage.
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
<svelte:window on:contextmenu|preventDefault={() => {}} />
