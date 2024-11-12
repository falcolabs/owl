<script lang="ts">
    import { Peeker, Connection, GameMaster, StateManager } from "$lib";
    import { readable, writable, type Readable } from "svelte/store";
    import Load from "../Load.svelte";
    import TitleBar from "../TitleBar.svelte";
    import VcnvMain from "./VCNVMain.svelte";
    import ShowAnswer from "../ShowAnswer.svelte";
    import ScoreBar from "../ScoreBar.svelte";
    import type { PlayerManager } from "$lib/player";

    export let conn: Connection;
    export let gm: GameMaster;
    export let states: StateManager;
    export let players: PlayerManager;
</script>

<title>Vượt chướng ngại vật - Đường đua xanh</title>
<div class="bg">
    <Load until={$states.selected !== undefined}>
        <TitleBar activity="Vượt chướng ngại vật" />
        <div class="center-box">
            {#if $states.show_key}
                <div class="answers">
                    <ShowAnswer {states} {players} />
                </div>
            {:else}
                <div class="main">
                    <VcnvMain {states} {conn} {gm} />
                </div>
            {/if}
        </div>
        <div class="bottom"><ScoreBar {players} {states} /></div>
    </Load>
</div>

<style>
    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .center-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        flex-direction: column;
        transform: translateY(2rem);
    }

    .bottom {
        position: absolute;
        transform: translateY(-5rem);
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
    }
</style>
