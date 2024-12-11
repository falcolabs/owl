<script lang="ts">
    import { SHOW_NAME, ORG_NAME, SUBTEXT, StateManager } from "$lib";
    import ScoreBar from "../ScoreBar.svelte";
    export let states: StateManager;
</script>

<div class="bg">
    <div class="titlegroup">
        <h2 class="caps">{ORG_NAME}</h2>
        <h1>
            {SHOW_NAME}
        </h1>
        <h2 class="caps subtext">{SUBTEXT}</h2>
    </div>
    <div class="bar"><ScoreBar {states} /></div>
</div>

<style>
    .bg {
        width: 100%;
        height: 100vh;
        background: var(--bg-gradient);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        overflow: hidden;
    }

    .titlegroup {
        display: flex;
        flex-direction: column;
        justify-self: center;
        align-items: center;

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
    .subtext {
        margin: 1rem;
    }

    .bar {
        position: fixed;
        bottom: 25px;

    }
</style>
