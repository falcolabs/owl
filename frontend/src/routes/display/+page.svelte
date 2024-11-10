<script lang="ts">
    import { Peeker, Connection, GameMaster, PlayerManager, StateManager } from "$lib";
    import { onMount } from "svelte";
    import Load from "../../components/Load.svelte";
    import KhoiDongDisplay from "../../components/display/KhoiDongDisplay.svelte";
    import VcnvDisplay from "../../components/display/VCNVDisplay.svelte";
    import TangTocDisplay from "../../components/display/TangTocDisplay.svelte";
    import VeDichDisplay from "../../components/display/VeDichDisplay.svelte";
    import Standby from "../../components/display/Standby.svelte";

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
                await gm.updateAll();
            }
        });
    });
</script>

<Load until={gm !== undefined && $states.__init}>
    {#if $states.available_parts[$states.current_part] == "khoidong"}
        <KhoiDongDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vcnv"}
        <VcnvDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "tangtoc"}
        <TangTocDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vedich"}
        <VeDichDisplay {conn} {gm} {states} {players} />
    {:else}
        <Standby />
    {/if}
</Load>
