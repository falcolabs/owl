<script lang="ts">
    import { Peeker, Connection, GameMaster } from "$lib";
    import { onMount } from "svelte";
    import Load from "../../components/Load";

    let conn: Connection;
    let gm: GameMaster;

    onMount(async () => {
        conn = await Connection.create();
    });
</script>
