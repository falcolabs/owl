<script lang="ts">
    import type { Writable } from "svelte/store";

    export let line: Writable<any>;
</script>

<div class="line">
    <div class="letter disabled">{$line.tag}</div>
    <div class="letter long disabled tag">{$line.content.length} ký tự</div>

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
        margin-right: 15px;
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

    .long {
        width: 100px;
        text-transform: unset;
        padding-left: 15px;
        padding-right: 15px;
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
