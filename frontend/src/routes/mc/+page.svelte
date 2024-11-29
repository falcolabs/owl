<script lang="ts">
    import {
        Peeker,
        Connection,
        GameMaster,
        PlayerManager,
        StateManager,
        ANTICHEAT_ENABLED
    } from "$lib";
    import { onMount } from "svelte";
    import Load from "../../components/Load.svelte";
    import KhoiDongDisplay from "../../components/mc/KhoiDongDisplay.svelte";
    import VcnvDisplay from "../../components/mc/VCNVDisplay.svelte";
    import TangTocDisplay from "../../components/mc/TangTocDisplay.svelte";
    import VeDichDisplay from "../../components/mc/VeDichDisplay.svelte";
    import Standby from "../../components/mc/Standby.svelte";
    import TieBreakerDisplay from "../../components/mc/TieBreakerDisplay.svelte";
    import Tkd from "../../components/display/TKD.svelte";
    import AntiCheat from "../../components/AntiCheat.svelte";

    let conn: Connection;
    let gm: GameMaster;
    let players: PlayerManager;
    let states: StateManager;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                gm.states.flush();
                await gm.updateAll();
            }
        });
    });
</script>

<div class:noselect={ANTICHEAT_ENABLED}>
    <Load until={gm !== undefined && $states.__init}>
        {#if $states.available_parts[$states.current_part] == "khoidong"}
            <KhoiDongDisplay {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "vcnv"}
            <VcnvDisplay {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tangtoc"}
            <TangTocDisplay {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "vedich"}
            <VeDichDisplay {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tiebreaker"}
            <TieBreakerDisplay {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tkd"}
            <Tkd {states} />
        {:else}
            <Standby />
        {/if}
        {#if ANTICHEAT_ENABLED}
            <AntiCheat url="" data={{}} />
        {/if}
    </Load>
</div>
