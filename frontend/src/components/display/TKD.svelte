<script lang="ts">
    import { StateManager } from "$lib";

    export let states: StateManager;
    console.log($states)
</script>

<div class="bg">
    <div class="container">
        {#each $states.engine_players as { identifier, name, score }}
            <div class="scoregroup" class:disappear={!Object.hasOwn($states.appear, identifier)}>
                <div class="name pill">{name}</div>
                <div class="score box prompt">{score}</div>
            </div>
        {/each}
    </div>
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

    .scoregroup.disappear {
        opacity: 0;
    }

    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 60px;
    }

    .scoregroup {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        transition: 200ms ease-in-out;
        opacity: 1;
    }

    .name {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 25px;
        width: fit-content;
        font-weight: bold;
        transform: translateY(-70px);
    }

    .score {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 50px 200px;
        font-weight: bold;
    }
</style>
