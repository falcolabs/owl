<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure, GameMaster } from "$lib";
    import type { Timer, Player } from "client";
    import { writable, readable, type Readable, type Writable } from "svelte/store";
    import SubmitJudger from "./SubmitJudger.svelte";
    import Load from "../Load.svelte";
    import TimerControls from "./TimerControls.svelte";
    export let states: StateManager;
    export let gm: GameMaster;
    export let conn: Connection;

    const isTile = (tile: string, s: string): boolean => {
        if (tile == "M") {
            return $states.puzzle_data.center.status == s;
        } else if (tile == "K") {
            return $states.puzzle_data.key.status == s;
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

<Load until={$states.puzzle_data !== undefined}>
    <div class="horizontal big-gap">
        <div class="vertical">
            <div>
                <h1>Game Master</h1>
                <button
                    class="btn"
                    class:accent={$states.show_key}
                    on:click={async () => {
                        if (!$states.show_key) {
                            await gm.sound.play("vcnv-showanswers");
                            console.log("2s delay before showing answer");
                            setTimeout(async () => {
                                await states.setBoolean("show_key", !$states.show_key);
                            }, 2000);
                        } else {
                            await states.setBoolean("show_key", !$states.show_key);
                        }
                    }}>{$states.show_key ? "ĐÁ thí sinh: HIỆN" : "ĐÁ thí sinh: ẨN"}</button
                >
                <button
                    class="btn"
                    class:accent={$states.final_hint}
                    on:click={async () =>
                        await states.setBoolean("final_hint", !$states.final_hint)}
                    >{$states.final_hint ? "Final Hint: Shown" : "Final Hint: Hidden"}</button
                >
                <button class="btn" on:click={async () => await states.setArray("highlighted", [])}
                    >Clear Bell</button
                >
            </div>
            <TimerControls
                {gm}
                onstart={async () => {
                    await gm.sound.play("vcnv-15secs");
                }}
                onreset={async () => {
                    await gm.sound.stop("vcnv-15secs");
                }}
            />
            <div>
                <h1>Thứ tự trả lời CNV</h1>
                {#each $states.highlighted as p}
                    <p>{p}</p>
                {/each}
            </div>
            <div class="vertical big-gap">
                <h1>Các hàng ngang</h1>
                <div class="vertical">
                    {#each [...$states.puzzle_data.normal.map(extractTag), "M", "K"] as r}
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
                                            if (op == "selected") {
                                                await gm.sound.play("vcnv-selectrow");
                                            }
                                            if (op == "shown") {
                                                await gm.sound.play("vcnv-open");
                                            }
                                        }
                                    }}
                                    >{op == "hidden"
                                        ? "ẩn"
                                        : op == "selected"
                                          ? "chọn"
                                          : op == "shown"
                                            ? "hiện"
                                            : "khóa"}</button
                                >
                            {/each}
                        </div>
                    {/each}
                </div>
            </div>
        </div>
    </div>
</Load>

<style>
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

    .btn:hover {
        filter: brightness(120%);
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

    .btn {
        margin: 0.5rem;
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

    h1 {
        font-weight: bold;
    }
</style>
