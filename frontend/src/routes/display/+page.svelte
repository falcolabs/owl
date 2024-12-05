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
    import KhoiDongDisplay from "../../components/display/KhoiDongDisplay.svelte";
    import VcnvDisplay from "../../components/display/VCNVDisplay.svelte";
    import TangTocDisplay from "../../components/display/TangTocDisplay.svelte";
    import VeDichDisplay from "../../components/display/VeDichDisplay.svelte";
    import Standby from "../../components/display/Standby.svelte";
    import TieBreakerDisplay from "../../components/display/TieBreakerDisplay.svelte";
    import Tkd from "../../components/display/TKD.svelte";
    import AntiCheat from "../../components/AntiCheat.svelte";
    import { SoundManager } from "$lib/sound";
    import type { Writable } from "svelte/store";

    let conn: Connection;
    let gm: GameMaster;
    let players: PlayerManager;
    let states: StateManager;
    let sound: SoundManager;
    let downloadText: Writable<string>;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        sound = await SoundManager.create(gm);
        downloadText = sound.downloadText;
        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                gm.states.flush();
                await gm.updateAll();
            }
        });
    });
</script>

<div class:noselect={ANTICHEAT_ENABLED}>
    <Load until={gm !== undefined && $states.__init && sound !== undefined}>
        {#if !sound.isReady}
            <p>{$downloadText}</p>
        {:else}
            {#if $states.engine_freeze}
                <Standby />
            {:else if $states.available_parts[$states.current_part] == "khoidong"}
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
        {/if}
    </Load>
</div>
