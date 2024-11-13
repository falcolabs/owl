<script lang="ts">
    import { Connection, type StateManager, CallProcedure } from "$lib";
    export let states: StateManager;
    export let conn: Connection;
    export let prefix: string;
</script>

<div>
    <div class="vertical">
        <p class="code">TODO - move this to judges' panel</p>
        <h1>Judges' Panel</h1>
        {#if $states.answers.length == 0}
            <p>No answers submitted</p>
        {:else}
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
                            {#each [true, false] as r}
                                <button
                                    class="btn smol code"
                                    class:accent={verdict == r}
                                    on:click={async () => {
                                        if (verdict == r) {
                                            await conn.send(
                                                CallProcedure.name(`${prefix}::verdict`)
                                                    .string("target", name)
                                                    .string("verdict", "null")
                                                    .build()
                                            );
                                        } else {
                                            await conn.send(
                                                CallProcedure.name(`${prefix}::verdict`)
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
        {/if}
    </div>
</div>

<style>
    h1 {
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
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

    .disabled-btn {
        cursor: default;
        background: none;
    }

    .disabled-btn:hover {
        filter: none;
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
