<script lang="ts">
    import type { StateManager } from "$lib";
    import { onMount } from "svelte";
    import BareTimer from "./BareTimer.svelte";
    import { writable } from "svelte/store";

    export let states: StateManager;
    const PRESETS: KeyframeAnimationOptions = {
        easing: "ease-in-out",
        fill: "both",
        duration: 200
    };

    let progress = writable(1);

    let timer = states.timerStore;
    onMount(() => {
        setInterval(() => {
            let max = $states.max_time;
            $progress = (max - $timer.elapsedSecs()) / max;
        }, 100);
    });
</script>

<BareTimer {progress} />
