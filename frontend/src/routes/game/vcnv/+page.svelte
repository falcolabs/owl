<script lang="ts">
    import { Peeker, Connection, GameMaster } from "$lib";
    import { onMount } from "svelte";
    import { readable, type Readable } from "svelte/store";
    import Load from "../../../components/Load.svelte";

    let conn: Connection;
    let gm: GameMaster;
    let states: Readable<any> = readable({

    })

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states
    });
</script>

<title>Vượt chướng ngại vật - Đường đua xanh</title>
<div class="bg">
    <Load until={gm !== undefined}>

    </Load>
</div>
