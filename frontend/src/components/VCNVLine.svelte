<script lang="ts">
    export let content: string;
    export let status: "hidden" | "selected" | "shown" | "disabled";
    export let tag: string;
</script>

<div class="line">
    <div class="letter disabled tag">{tag}</div>
    {#each content as lett}
        <div class="letter" class:selected={status == "selected"} class:shown={status == "shown"} class:disabled={status == "disabled"}>{lett}</div>
    {/each}
</div>

<style>
    .line {
        display: flex;
        flex-direction: row;
        column-gap: 15px;
    }

    .tag {
        margin-right: 30px;
    }

    .letter {
        /* TODO - allow theming with variables */
        background-color: #7379a2;
        text-transform: uppercase;
        width: 48px;
        height: 48px;
        border-radius: 13px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }

    .selected {
        /* TODO - allow theming with variables */
        background-color: #6979ea;
    }

    .shown {
        /* TODO - allow theming with variables */
        background-color: #9ca6ec;
    }

    .disabled {
        background-color: var(--bg-dark-1);
    }

</style>
