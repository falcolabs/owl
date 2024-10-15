<script lang="ts">
    import { Peeker, Connection, GameMaster, PlayerManager } from "$lib";
    import { type Readable } from "svelte/store";
    import { onMount } from "svelte";
    import Load from "../../components/Load.svelte";
    import KhoiDongDisplay from "../../components/display/KhoiDongDisplay.svelte";
    import VcnvDisplay from "../../components/display/VCNVDisplay.svelte";
    import TangTocDisplay from "../../components/display/TangTocDisplay.svelte";
    import VeDichDisplay from "../../components/display/VeDichDisplay.svelte";
    import AuthPlayer from "../../components/player/AuthPlayer.svelte";

    let conn: Connection;
    let gm: GameMaster;
    let players: PlayerManager;
    let states: Readable<any>;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        conn.on(Peeker.PacketType.UpdateState, async (update) => {
            if (update.value.name === "current_part") {
                await gm.updateAll();
            }
        });
    });
</script>

<Load until={gm !== undefined && $states.__init}>
    {#if $states.available_parts[$states.current_part] == "auth"}
        <AuthPlayer />
    {:else if $states.available_parts[$states.current_part] == "khoidong"}
        <KhoiDongDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vcnv"}
        <VcnvDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "tangtoc"}
        <TangTocDisplay {conn} {gm} {states} {players} />
    {:else if $states.available_parts[$states.current_part] == "vedich"}
        <VeDichDisplay {conn} {gm} {states} {players} />
        <!-- {:else if $states.available_parts[$states.current_part] == "standby"}
        <StandbyDisplay {conn} {gm} {states} {players} /> -->
    {/if}
</Load>
