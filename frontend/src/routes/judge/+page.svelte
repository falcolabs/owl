<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, GameMaster, StateManager, Peeker } from "$lib";
    import type { Player } from "client";
    import Load from "../../components/Load.svelte";
    import { readable, writable, type Writable, type Readable } from "svelte/store";
    import ScoreJudge from "../../components/panel/ScoreJudge.svelte";
    import SubmitJudger from "../../components/panel/SubmitJudger.svelte";
    import KhoiDong from "../../components/judge/KhoiDong.svelte";

    let conn: Connection;
    let gm: GameMaster;
    // @ts-ignore
    let players: Readable<Map<string, Player>> = readable(new Map());
    let states: StateManager;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;

        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                // @ts-ignore
                states = undefined;
                await gm.updateAll();
                states = gm.states;
            }
        });
    });
</script>

<div class="bg">
    <Load until={gm !== undefined && states !== undefined && $states.engine_players !== undefined}>
        <div class="container">
            <p class="qdisplay prompt">{$states.prompt == undefined ? "" : $states.prompt}</p>
            {#if $states.key !== undefined}
                <p class="qdisplay tag">{$states.key}</p>
            {/if}
            <div class="center">
                <ScoreJudge {conn} {states} {gm} />
                {#if $states.available_parts[$states.current_part] == "vcnv" || $states.available_parts[$states.current_part] == "tangtoc"}
                    <SubmitJudger
                        {conn}
                        {states}
                        prefix={$states.available_parts[$states.current_part]}
                    />
                {/if}
                {#if $states.available_parts[$states.current_part] == "khoidong"}
                    <KhoiDong {conn} {gm} {states} />
                {/if}
            </div>
        </div>
    </Load>
</div>

<style>
    .container {
        display: flex;
        flex-direction: column;
        width: fit-content;
        align-items: center;
        justify-content: center;
        width: 100%;
        height: 100vh;
        gap: 30px;
    }

    .center {
        display: flex;
        flex-direction: row;
        width: fit-content;
        align-items: center;
        justify-content: center;
        width: 100%;
        gap: 100px;
    }

    .qdisplay {
        max-width: 60vw;
        text-align: center;
    }

    .bg {
        position: fixed;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: var(--bg-dark-1);
    }
</style>
