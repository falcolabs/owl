<script lang="ts">
    import { Connection, Peeker, type StateManager, CallProcedure, GameMaster } from "$lib";
    import { scoreOf } from "$lib/globals";
    import { getAllContexts } from "svelte";
    import Load from "../Load.svelte";
    import TimerControls from "./TimerControls.svelte";
    export let states: StateManager;
    export let gm: GameMaster;
    export let conn: Connection;

    const STAGE_CHOOSE: number = 0;
    const STAGE_COMPETE: number = 1;
</script>

<Load until={$states.package !== undefined}>
    <div class="vertical">
        <div class="vertical">
            <h1>Game Master</h1>
            <button
                class="btn"
                on:click={async () => {
                    if ($states.qid == -1) {
                        await states.setNumber(
                            "qid",
                            $states.placement[$states.current_player_username][0]
                        );
                    } else {
                        let a = $states.placement[$states.current_player_username];
                        let newIndex = Array.from(a).indexOf($states.qid) + 1;
                        if (newIndex > 2) {
                            await states.setNumber("qid", -1);
                        } else {
                            await states.setNumber("qid", a[newIndex]);
                        }
                    }
                }}>Next question</button
            >
            <button
                class="btn"
                class:accent={$states.stage == STAGE_CHOOSE}
                on:click={async () => {
                    if ($states.stage == STAGE_CHOOSE) {
                        await gm.sound.play("vedich-confirmchoice");
                    }
                    await states.setNumber(
                        "stage",
                        $states.stage == STAGE_CHOOSE ? STAGE_COMPETE : STAGE_CHOOSE
                    );
                }}>{$states.stage == STAGE_CHOOSE ? "Chọn gói" : "Câu hỏi"}</button
            >
            <button
                class="btn"
                on:click={async () => {
                    await states.setString("bell_player", "");
                }}>Xóa chuông</button
            >
            <button
                class="btn"
                class:accent={$states.allow_bell}
                on:click={async () => {
                    if (!$states.allow_bell) {
                        await gm.sound.play("vedich-poll");
                    } else {
                        await gm.sound.stop("vedich-poll");
                    }
                    await states.setBoolean("allow_bell", !$states.allow_bell);

                    setTimeout(async () => {
                        await states.setBoolean("allow_bell", false);
                    }, 5000);
                }}>{$states.allow_bell ? "Chuông bật (tự tắt)" : "Chuông tắt"}</button
            >
            {#if $states.media != null}
                <button
                    class="btn"
                    class:accent={$states.media_status.visible}
                    on:click={async () => {
                        let status = $states.media_status;
                        status.visible = !status.visible;
                        await states.setObject("media_status", status);
                    }}>{$states.media_status.visible ? "Ẩn media" : "Hiện media"}</button
                >
            {/if}
        </div>
        <TimerControls
            {gm}
            onstart={async () => {
                switch ($states.max_time) {
                    case 15:
                        await gm.sound.play("vedich-15secs");
                        break;
                    case 20:
                        await gm.sound.play("vedich-20secs");
                        break;
                    case 40:
                        await gm.sound.play("tangtoc-40secs");
                        break;
                }
            }}
        />
        <div class="vertical">
            <h1>Thí sinh</h1>
            <div class="horizontal">
                <button
                    class="btn smol nomargin-horizontal"
                    class:accent={$states.current_player_username == ""}
                    on:click={async () => {
                        await states.setString("current_player_username", "");
                        await states.setNumber("stage", STAGE_CHOOSE);
                    }}>unset</button
                >
                {#each Object.keys($states.package) as ident}
                    <button
                        class="btn smol nomargin-horizontal"
                        class:accent={$states.current_player_username == ident}
                        on:click={async () => {
                            await gm.sound.play("vedich-packagechoice");
                            await states.setString("current_player_username", ident);
                            await states.setNumber("stage", STAGE_CHOOSE);
                        }}>{ident}</button
                    >
                {/each}
            </div>
            {#if $states.current_player_username !== ""}
                <div class="vertical">
                    <h1>Gói câu hỏi cho {$states.current_player_username}:</h1>
                    {#each [0, 1, 2] as i}
                        <div class="horizontal smolmargin">
                            {#each [0, 20, 30] as score}
                                <button
                                    class="btn smol nomargin"
                                    class:accent={$states.package[$states.current_player_username][
                                        i
                                    ] == score}
                                    on:click={async () => {
                                        await conn.send(
                                            CallProcedure.name("vedich::set_choice")
                                                .string("target", $states.current_player_username)
                                                .number("slot", i)
                                                .number("to", score)
                                                .build()
                                        );
                                    }}>{score != 0 ? score : "unset"}</button
                                >
                            {/each}
                        </div>
                    {/each}
                    <!-- TODO -->
                    <!-- <h1>Media Controls</h1> -->
                </div>
                <div class="horizontal big-gap">
                    <div class="vertical">
                        <h1>Câu hỏi</h1>
                        <div class="horizontal">
                            <button
                                class="btn smol nomargin-horizontal"
                                class:accent={$states.qid == -1}
                                on:click={async () => await states.setNumber("qid", -1)}
                                >unset</button
                            >
                            {#each $states.placement[$states.current_player_username] as qid}
                                <button
                                    class="btn smol nomargin-horizontal"
                                    class:accent={qid == $states.qid && qid != -1}
                                    on:click={async () => await states.setNumber("qid", qid)}
                                    ><span class="bold">{qid == -1 ? "unset" : qid}</span>{qid == -1
                                        ? ""
                                        : `: ${scoreOf[qid]}đ`}</button
                                >
                            {/each}
                        </div>
                    </div>
                    <div class="vertical">
                        <h1>Ngôi sao hy vọng</h1>
                        <div class="horizontal">
                            {#each $states.placement[$states.current_player_username] as qid}
                                <button
                                    class="btn smol nomargin-horizontal"
                                    class:accent={$states.hope_stars.includes(qid) && qid != -1}
                                    on:click={async () => {
                                        let hs = $states.hope_stars;
                                        if (hs.includes(qid)) {
                                            const index = hs.indexOf(qid);
                                            hs.splice(index, 1);
                                            await gm.sound.stop("vedich-star");
                                        } else {
                                            hs.push(qid);
                                            await gm.sound.play("vedich-star");
                                        }
                                        await states.setArray("hope_stars", hs);
                                    }}>{qid == -1 ? "unset" : qid}</button
                                >
                            {/each}
                        </div>
                    </div>
                </div>
            {:else}
                <p>Chưa chọn thí sinh nào</p>
            {/if}
        </div>
    </div>
    <div>
        <p>Câu {$states.qid}. {$states.prompt}</p>
        <p style="font-weight: bold;">{$states.key}</p>
    </div>
</Load>

<style>
    h1 {
        font-weight: bold;
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

    .bold {
        font-weight: bold;
    }

    .btn:hover {
        filter: brightness(120%);
    }

    .nomargin {
        margin: 0;
    }

    .smolmargin {
        margin: 5px;
    }

    .accent {
        background-color: var(--accent);
    }

    .nomargin-horizontal {
        margin-left: 0;
        margin-right: 0;
    }

    .smol {
        padding: 15px;
        font-size: 1em;
        border-radius: 13px;
        border: none;
    }

    .horizontal {
        display: flex;
        flex-direction: row;
        gap: 5px;
    }

    .big-gap {
        gap: 25px;
    }
</style>
