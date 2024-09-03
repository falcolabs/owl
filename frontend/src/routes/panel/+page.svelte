<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, Peeker, CallProcedure, Push, GameMaster, StateManager } from "$lib";
    import type { Timer, Player } from "client";
    import Load from "../../components/Load.svelte";
    import { readable, writable, get, type Writable, type Readable } from "svelte/store";
    import ScoreBar from "../../components/ScoreBar.svelte";
    import KhoiDong from "../../components/panel/KhoiDong.svelte";

    let conn: Connection;
    let gm: GameMaster;
    // @ts-ignore
    let timer: Writable<Timer> = writable({ elapsedSecs: () => 6.9 });
    let players: Readable<Map<string, Player>> = readable(new Map());
    let elapsed = writable("0.00");
    // @ts-ignore
    let states: StateManager

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;

        timer = states.timerStore;
        setInterval(() => {$elapsed = $timer.elapsedSecs().toFixed(2)}, 100)
    });

</script>

<div class="bg">
    <Load until={gm !== undefined}>
        <div class="container">
            <h1>Trash control panel</h1>
            <ScoreBar gamemaster={gm} />
            <KhoiDong {states} {conn} {elapsed} {players} />
        </div>
    </Load>
</div>

<style>
    h1 {
        font-size: var(--font-large);
        font-weight: bold;
        width: fit-content;
    }

    .container {
        display: flex;
        flex-direction: column;
        gap: 25px;
        width: fit-content;
    }

    .bg {
        position: fixed;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: var(--bg-dark-1);
        padding: 2em;
    }
</style>
