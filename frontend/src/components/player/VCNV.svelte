<script lang="ts">
    import { Peeker, Connection, GameMaster, StateManager, CallProcedure } from "$lib";
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
            <div class="bottom">
                <button
                    class="btn answercnv"
                    class:activated={$states.highlighted.includes(gm.username)}
                    on:click={async () => {
                        await conn.send(CallProcedure.name("vcnv::bell").string("token", gm.authToken).number("timeMs", Date.now()).build());
                    }}>Chuông trả lời CNV</button
                >
                <ScoreBar {states} />
            </div>
        </div>
    </Load>
</div>

<style>
    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--bg-dark-2);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: fit-content;
    }

    .activated {
        background-color: var(--accent);
    }

    .btn:hover {
        background-color: var(--accent);
    }

    .center-box {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100vh;
        flex-direction: column;
        transform: translateY(4rem);
    }

    .bottom {
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15vw;
    }
</style>
