<script lang="ts">
    import { CallProcedure, type Connection } from "$lib";

    export let conn: Connection;
</script>

<div>
    <h1>Quản lý hiện điểm</h1>
    <button class="btn" on:click={async () => {
        await conn.send(CallProcedure.name("tkd::show_next").build())
    }}>Hiện tiếp</button>
</div>

<style>
    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1rem;
        margin: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--bg-dark-2);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: fit-content;
    }

    h1 {
        font-weight: bold;
    }

    .btn:hover {
        filter: brightness(90%);
    }
</style>
