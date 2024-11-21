<script lang="ts">
    import type { Writable } from "svelte/store";

    export let line: Writable<any>;
    console.log($line);
</script>

<div class="line">
    <div class="letter disabled tag">{$line.tag}</div>
    {#each $line.content as lett}
        <div
            class="letter"
            class:selected={$line.status == "selected"}
            class:shown={$line.status == "shown"}
            class:disabled={$line.status == "disabled"}
        >
            <span class:hide={$line.status != "shown"}>{lett}</span>
        </div>
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
        transition: 200ms ease-in-out;
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

    .hide {
        display: none;
    }
</style>
