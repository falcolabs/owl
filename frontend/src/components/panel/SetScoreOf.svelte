<script lang="ts">
    import { CallProcedure, type Connection, type PlayerManager } from "$lib";
    import { onMount } from "svelte";

    export let conn: Connection;
    export let identifier: string;
    export let players: PlayerManager;
    let score;
    let inp: number;

    const refreshScore = () => {
        inp = players.name(identifier).score;
    };

    onMount(() => {});
</script>

<form on:submit={async () => {
    await conn.send(CallProcedure.name("engine::set_score").string("target", identifier).number("value", inp).build())
}}>
    <input type="number" on:input={(v) => {}} bind:value={inp} />
</form>
