<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, Peeker, RPCBuilder } from "$lib";

    class Test {
        hi?: string;
    }

    onMount(async () => {
        let conn = await Connection.create();
        conn.on("*", (packet) => {
            console.log(packet.value);
        });
        await conn.send(Peeker.Query.availableProcedures()).then(() => {
            console.log("Sent message.");
        });
        await conn.send(new RPCBuilder().name("khoidong::setstate_seperated").build())
    });
</script>
