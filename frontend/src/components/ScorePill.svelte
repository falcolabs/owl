<script lang="ts">
    export let activated: boolean;
    export let name: string;
    export let score: number;
</script>

{#if activated}
    <div class="score-pill tag activated">
        <p>{name}</p>
        <p>{score}</p>
    </div>
{:else}
    <div class="score-pill tag">
        <p>{name}</p>
        <p>{score}</p>
    </div>
{/if}

<style>
    .score-pill {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        width: 9em;
        /* height: 60px; */
        border-radius: 18px;
        box-shadow: 0 4px 4px 0 #00000040;
        border: solid 1px #6a72b4;
        background-color: #2a3164;
        padding: 18px 23px;
    }

    .activated {
        background-image: linear-gradient(to right, #e3599a 0%, #956bea 100%);
    }
</style>
