<script lang="ts">
    import { type Connection, type StateManager, CallProcedure, GameMaster } from "$lib";
    import Load from "../Load.svelte";
    import ScorePillSmall from "../ScorePillSmall.svelte";
    import SetScoreOf from "./SetScoreOf.svelte";

    export let conn: Connection;
    export let gm: GameMaster;
    export let states: StateManager;
</script>

<div class="bar">
    {#if $states.highlighted !== undefined}
        {#each $states.engine_players as player}
            <Load until={$states.plusminus !== undefined}>
                <div class="scorestack">
                    {#each $states.plusminus.rem as i}
                        <button
                            class="btn destructive"
                            on:click={async () => {
                                await conn.send(
                                    CallProcedure.name("engine::add_score")
                                        .string("target", player.identifier)
                                        .number("value", i)
                                        .build()
                                );
                            }}>{i}</button
                        >
                    {/each}
                    <ScorePillSmall
                        activated={$states.highlighted.includes(player.identifier)}
                        name={player.name}
                        score={player.score}
                    />
                    <SetScoreOf {conn} identifier={player.identifier} players={gm.players} {states}/>

                    {#each $states.plusminus.add as i}
                        <button
                            class="btn"
                            on:click={async () => {
                                console.log(
                                    CallProcedure.name("engine::add_score")
                                        .string("target", player.identifier)
                                        .number("value", i)
                                        .build()
                                        .pack()
                                );
                                await conn.send(
                                    CallProcedure.name("engine::add_score")
                                        .string("target", player.identifier)
                                        .number("value", i)
                                        .build()
                                );
                            }}>+{i}</button
                        >
                    {/each}
                </div>
            </Load>
        {/each}
    {/if}
</div>

<style>
    .bar {
        display: flex;
        flex-direction: row;
        gap: 25px;
        width: fit-content;
        justify-content: flex-start;
        align-items: flex-start;
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
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: 100%;
    }
    .btn:hover {
        background-color: var(--accent);
    }

    .destructive:hover {
        background-color: #f35d5d;
    }

    .scorestack {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>
