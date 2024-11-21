<script lang="ts">
    import type { StateManager } from "$lib";
    import { onMount } from "svelte";
    import type { Readable } from "svelte/store";

    let thumb: HTMLDivElement;
    export let progress: Readable<number>;

    onMount(() => {
        progress.subscribe((v) => {
            if (thumb === null) return;
            if (v >= 1) {
                thumb.style.width = "100%";
            } else {
                thumb.style.width = `${v * 100}%`;
            }
            thumb.style.display = v <= 0 ? "none" : "block";
        });
    });
</script>

<div class="timerbar">
    <div class="thumb" bind:this={thumb} />
</div>

<style>
    .timerbar {
        width: 100%;
        max-width: 100%;
        height: 11px;
        border-radius: 9px;
        border: 1px solid var(--border-color);
    }

    .thumb {
        background-color: var(--accent);
        border-radius: 9px;
        height: 100%;
        transition: 100ms linear;
    }
</style>
