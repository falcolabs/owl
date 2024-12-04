<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, GameMaster, StateManager, Peeker, CallProcedure } from "$lib";
    import type { Timer, Player } from "client";
    import Load from "../../components/Load.svelte";
    import { readable, writable, get, type Writable, type Readable } from "svelte/store";
    import KhoiDong from "../../components/panel/KhoiDong.svelte";
    import Vcnv from "../../components/panel/VCNV.svelte";
    import TimerControls from "../../components/panel/TimerControls.svelte";
    import TangToc from "../../components/panel/TangToc.svelte";
    import VeDich from "../../components/panel/VeDich.svelte";
    import PartSwitcher from "../../components/panel/PartSwitcher.svelte";
    import ScoreJudge from "../../components/panel/ScoreJudge.svelte";
    import TieBreaker from "../../components/panel/TieBreaker.svelte";
    import Tkd from "../../components/panel/TKD.svelte";

    let conn: Connection;
    let gm: GameMaster;
    // @ts-ignore
    let players: Readable<Map<string, Player>> = readable(new Map());
    let elapsed = writable("0.00");
    let states: StateManager;
    let time: Writable<number>;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        time = states.time;

        setInterval(async () => {
            let e = $time;
            if ($states.max_time !== undefined) {
                if ($states.max_time - e <= 0) {
                    $elapsed = "0";
                    if (!$states.timer_paused) {
                        await gm.timer_operation("pause");
                    }
                } else {
                    $elapsed = ($states.max_time - e).toFixed(2);
                }
            } else {
                $elapsed = `Video progress: ${e.toFixed(2)}`;
            }
        }, 100);

        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                await gm.updateAll();
            }
        });
    });
</script>

<div class="bg">
    <Load until={gm !== undefined && $states.available_parts !== undefined}>
        <div class="container">
            <h1>Trash control panel</h1>
            <div class="horizontal">
                <div>
                    <TimerControls {elapsed} {gm} {states} {conn} />
                    <div class="partcontrol">
                        {#if $states.available_parts[$states.current_part] == "khoidong"}
                            <KhoiDong {gm} {states} {conn} {players} />
                        {:else if $states.available_parts[$states.current_part] == "vcnv"}
                            <Vcnv {states} {conn} />
                        {:else if $states.available_parts[$states.current_part] == "tangtoc"}
                            <TangToc {states} {conn} {gm} />
                        {:else if $states.available_parts[$states.current_part] == "vedich"}
                            <VeDich {states} {conn} />
                        {:else if $states.available_parts[$states.current_part] == "tiebreaker"}
                            <TieBreaker {states} {conn} {players} />
                        {:else if $states.available_parts[$states.current_part] == "tkd"}
                            <Tkd {conn} />
                        {/if}
                    </div>
                </div>
                <div class="right">
                    <PartSwitcher {states} {conn} />
                    <ScoreJudge {conn} {states} {gm} />
                </div>
            </div>
        </div>
    </Load>
</div>

<style>
    h1 {
        font-size: var(--font-large);
        font-weight: bold;
        width: fit-content;
    }

    .partcontrol {
        max-width: 50vw;
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

    .right {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .horizontal {
        display: grid;
        grid-template-columns: 50vw 50vw;
        flex-direction: row;
        gap: 15px;
    }
</style>
