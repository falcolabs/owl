<script lang="ts">
    import { Peeker, Connection, GameMaster, PlayerManager, StateManager } from "$lib";
    import { type Readable } from "svelte/store";
    import { onMount } from "svelte";
    import Load from "../../components/Load.svelte";
    import TangTocDisplay from "../../components/display/TangTocDisplay.svelte";
    import VeDichDisplay from "../../components/display/VeDichDisplay.svelte";
    import AuthPlayer from "../../components/player/AuthPlayer.svelte";
    import Standby from "../../components/display/Standby.svelte";
    import KhoiDong from "../../components/player/KhoiDong.svelte";
    import Vcnv from "../../components/player/VCNV.svelte";

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
    {#if $states.available_parts[$states.current_part] == "standby"}
        <Standby />
    {:else if $states.available_parts[$states.current_part] == "auth"}
        <!-- TODO - SECURITY: make this login portal always show up when unauthenticated -->
        <AuthPlayer {gm} />
    {:else if $states.available_parts[$states.current_part] == "khoidong"}
        <KhoiDong {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vcnv"}
        <Vcnv {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "tangtoc"}
        <TangTocDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vedich"}
        <VeDichDisplay {conn} {gm} {states} {players} />
    {/if}
</Load>
