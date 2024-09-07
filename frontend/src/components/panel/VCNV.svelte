<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure } from "$lib";
    import type { Timer, Player } from "client";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    export let states: StateManager;
    export let conn: Connection;
    export let players: Readable<Map<string, Player>>;

    const isTile = (tile: string, s: string): boolean => {
        console.log(tile, s);
        if (tile == "M") {
            return $states.puzzle_data.center.status == s;
        } else {
            for (let td of $states.puzzle_data.normal) {
                if (td["tag"] == tile) {
                    return td["status"] == s;
                }
            }
        }

        return false;
    };

    const extractTag = (td: { tag: string }) => td.tag;
</script>

<div class="horizontal big-gap">
    <div class="vertical">
        <div>
            <h1>GameMaster Controls</h1>
            <button
                class="btn"
                class:accent={$states.show_key}
                on:click={async () => await states.setBoolean("show_key", !$states.show_key)}
                >{$states.show_key ? "Key: Shown" : "Key: Hidden"}</button
            >
            <button
                class="btn"
                class:accent={$states.final_hint}
                on:click={async () => await states.setBoolean("final_hint", !$states.final_hint)}
                >{$states.final_hint ? "Final Hint: Shown" : "Final Hint: Hidden"}</button
            >
        </div>
        <div class="vertical big-gap">
            <h1>Selected Row</h1>
            <div class="vertical">
                {#each [...$states.puzzle_data.normal.map(extractTag), "M"] as r}
                    <div class="horizontal">
                        <div class="btn disabled-btn smol code">
                            {r}
                        </div>
                        {#each ["hidden", "selected", "shown", "disabled"] as op}
                            <button
                                class="btn smol code"
                                class:accent={isTile(r, op)}
                                on:click={async () => {
                                    if (isTile(r, op)) {
                                        // Click again to hide
                                        await conn.send(
                                            CallProcedure.name("vcnv::update_tiles")
                                                .string("target", r)
                                                .string("status", "hidden")
                                                .build()
                                        );
                                    } else {
                                        await conn.send(
                                            CallProcedure.name("vcnv::update_tiles")
                                                .string("target", r)
                                                .string("status", op)
                                                .build()
                                        );
                                    }
                                }}>{op}</button
                            >
                        {/each}
                    </div>
                {/each}
            </div>
        </div>
    </div>
    <div class="vertical">
        <p class="code">TODO - move this to judges' panel</p>
        {#each $states.answers as { time, name, content }}
            <p class="code">{time.toFixed(2).padStart(5, "0")} {name}: {content}</p>
        {/each}

        <div class="horizontal">
            <div class="vertical">
                {#each $states.answers as { name }}
                    <p class="btn disabled-btn smol code">{name}</p>
                {/each}
            </div>
            <div class="vertical">
                {#each $states.answers as { name, verdict }}
                    <div class="horizontal">
                        {#each [true, false, null] as r}
                            <button
                                class="btn smol code"
                                class:accent={verdict == r}
                                on:click={async () => {
                                    if (verdict == r) {
                                        await conn.send(
                                            CallProcedure.name("vcnv::verdict")
                                                .string("target", name)
                                                .string("verdict", "null")
                                                .build()
                                        );
                                    } else {
                                        await conn.send(
                                            CallProcedure.name("vcnv::verdict")
                                                .string("target", name)
                                                .string("verdict", JSON.stringify(r))
                                                .build()
                                        );
                                    }
                                }}>{r}</button
                            >
                        {/each}
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>

<style>
    .btn {
        font-family: var(--font);
        font-size: var(--font-normal);
        color: var(--text);
        padding: 1rem;
        margin: 1rem;
        margin-left: 0;
        user-select: none;
        cursor: pointer;
        background-color: var(--bg-dark-2);
        border: 2px var(--accent) solid;
        border-radius: var(--radius-1);
        transition: 100ms ease-in-out;
        width: fit-content;
    }

    .btn:hover {
        filter: brightness(120%);
    }

    td {
        border-spacing: none;
    }

    .disabled-btn {
        cursor: default;
        background: none;
    }

    .disabled-btn:hover {
        filter: none;
    }

    div.big-gap {
        gap: 15px;
    }

    .small-margin-bottom {
        margin-bottom: 5px;
    }

    .vertical {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .horizontal {
        display: flex;
        flex-direction: row;
        gap: 5px;
    }

    .accent {
        background-color: var(--accent);
    }

    .smol {
        padding: 15px;
        margin: 0;
        font-size: 1em;
        border-radius: 9px;
        border: none;
    }

    .code {
        font-family: var(--font-monospace);
    }
</style>
