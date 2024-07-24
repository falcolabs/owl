<script lang="ts">
    import { SHOW_NAME, ORG_NAME } from "$lib";

    export let activity: string;
</script>

<div class="container">
    <h2 class="caps">{ORG_NAME}</h2>
    <h1>
        {SHOW_NAME}
        {#if activity != ""}
            <span> · {activity}</span>
        {/if}
    </h1>
</div>

<style>
    .caps {
        text-transform: uppercase;
        margin-bottom: 0.5em;
    }

    .container {
        margin-top: 25px;
        margin-left: 100px;
        position: absolute;
    }

    h2 {
        font-size: 1.5rem;
        color: var(--text-2);
        font-weight: bold;
    }
    h1 {
        font-size: 2.5rem;
        color: var(--text);
        font-weight: bold;
    }

    span {
        font-weight: normal;
    }
</style>
