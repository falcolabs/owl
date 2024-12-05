<script lang="ts">
    import {
        Peeker,
        Connection,
        GameMaster,
        PlayerManager,
        StateManager,
        ANTICHEAT_ENABLED
    } from "$lib";
    import { writable, type Readable, type Writable } from "svelte/store";
    import { onMount } from "svelte";
    import Load from "../../components/Load.svelte";
    import AuthPlayer from "../../components/player/AuthPlayer.svelte";
    import Standby from "../../components/display/Standby.svelte";
    import KhoiDong from "../../components/player/KhoiDong.svelte";
    import Vcnv from "../../components/player/VCNV.svelte";
    import TangToc from "../../components/player/TangToc.svelte";
    import VeDich from "../../components/player/VeDich.svelte";
    import TieBreaker from "../../components/player/TieBreaker.svelte";
    import Tkd from "../../components/display/TKD.svelte";
    import AntiCheat from "../../components/AntiCheat.svelte";

    let conn: Connection;
    let gm: GameMaster;
    let players: PlayerManager;
    let states: StateManager;
    let isAuthenticated: Writable<boolean> = writable(false);
    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        isAuthenticated = gm.isAuthenticated;
        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                states.flush();
                await gm.updateAll();
            }
        });
    });
</script>

<div class:noselect={ANTICHEAT_ENABLED}>
    <Load until={gm !== undefined && $states.__init}>
        {#if !isAuthenticated}
            <AuthPlayer {gm} />
        {:else if $states.available_parts[$states.current_part] == "standby" || $states.engine_freeze}
            <Standby />
        {:else if $states.available_parts[$states.current_part] == "auth"}
            <!-- TODO - SECURITY: make this login portal always show up when unauthenticated -->
            <AuthPlayer {gm} />
        {:else if $states.available_parts[$states.current_part] == "khoidong"}
            <KhoiDong {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "vcnv"}
            <Vcnv {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tangtoc"}
            <TangToc {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "vedich"}
            <VeDich {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tiebreaker"}
            <TieBreaker {conn} {gm} {states} {players} />
        {:else if $states.available_parts[$states.current_part] == "tkd"}
            <Tkd {states} />
        {/if}
        {#if ANTICHEAT_ENABLED}
            <AntiCheat url="" data={{}} />
        {/if}
    </Load>
</div>
