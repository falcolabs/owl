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
    h1 {
        font-weight: bold;
    }
</style>
