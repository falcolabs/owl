<script lang="ts">
    import { onMount } from "svelte";
    import { Connection, GameMaster, StateManager, Peeker, CallProcedure } from "$lib";
    import type { Timer, Player } from "client";
    import Load from "../../components/Load.svelte";
    import { readable, writable, get, type Writable, type Readable } from "svelte/store";
    import KhoiDong from "../../components/panel/KhoiDong.svelte";
    import Vcnv from "../../components/panel/VCNV.svelte";
    import TimerControls from "../../components/panel/TimerControls.svelte";
    import TangToc from "../../components/panel/TangToc.svelte";
    import VeDich from "../../components/panel/VeDich.svelte";
    import PartSwitcher from "../../components/panel/PartSwitcher.svelte";
    import TieBreaker from "../../components/panel/TieBreaker.svelte";
    import Tkd from "../../components/panel/TKD.svelte";
    import SoundBoard from "../../components/panel/SoundBoard.svelte";

    let conn: Connection;
    let gm: GameMaster;
    // @ts-ignore
    let players: Readable<Map<string, Player>> = readable(new Map());
    let elapsed = writable("0.00");
    let states: StateManager;
    let time: Writable<number>;

    onMount(async () => {
        conn = await Connection.create();
        gm = await GameMaster.create(conn);
        states = gm.states;
        players = gm.players;
        time = states.time;

        setInterval(async () => {
            let e = $time;
            if ($states.max_time !== undefined) {
                if ($states.max_time - e <= 0) {
                    $elapsed = "0";
                    if (!$states.timer_paused) {
                        await gm.timer_operation("pause");
                    }
                } else {
                    $elapsed = ($states.max_time - e).toFixed(2);
                }
            } else {
                $elapsed = `Video progress: ${e.toFixed(2)}`;
            }
        }, 100);

        conn.on(Peeker.PacketType.State, async (update) => {
            if (update.value.name === "current_part") {
                await gm.updateAll();
            }
        });
    });
</script>

<div class="bg">
    <Load until={gm !== undefined && $states.available_parts !== undefined}>
        <div class="container">
            <div class="horizontal">
                <div>
                    <TimerControls {elapsed} {gm} {states} {conn} />

                    {#if $states.available_parts[$states.current_part] == "khoidong"}
                        <KhoiDong {gm} {states} {conn} {players} />
                    {:else if $states.available_parts[$states.current_part] == "vcnv"}
                        <Vcnv {gm} {states} {conn} />
                    {:else if $states.available_parts[$states.current_part] == "tangtoc"}
                        <TangToc {states} {conn} {gm} />
                    {:else if $states.available_parts[$states.current_part] == "vedich"}
                        <VeDich {gm} {states} {conn} />
                    {:else if $states.available_parts[$states.current_part] == "tiebreaker"}
                        <TieBreaker {states} {conn} {players} />
                    {:else if $states.available_parts[$states.current_part] == "tkd"}
                        <Tkd {conn} />
                    {/if}
                </div>
                <div class="right">
                    <PartSwitcher {states} {conn} />
                    <SoundBoard
                        {gm}
                        sounds={[
                            { displayName: "Chuyển phần", fileName: "common-startsection" },
                            { displayName: "Chỗ trống", fileName: "common-dotdotdot" }
                        ]}
                    />
                    {#if $states.available_parts[$states.current_part] == "khoidong"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Giới thiệu", fileName: "khoidong-start" },
                                { displayName: "Sẵn sàng", fileName: "khoidong-ready" },
                                { displayName: "3s", fileName: "khoidong-3secs" },
                                { displayName: "Nhạc nền", fileName: "khoidong-bgm" },
                                { displayName: "Đúng", fileName: "khoidong-correct" },
                                { displayName: "Sai", fileName: "khoidong-incorrect" },
                                { displayName: "Chuông", fileName: "khoidong-bell" },
                                { displayName: "Hoàn thành", fileName: "khoidong-complete" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "vcnv"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Giới thiệu", fileName: "vcnv-start" },
                                { displayName: "Chọn hàng", fileName: "vcnv-selectrow" },
                                { displayName: "15s", fileName: "vcnv-15secs" },
                                { displayName: "Đáp án", fileName: "vcnv-showanswers" },
                                { displayName: "Đúng", fileName: "vcnv-correct" },
                                { displayName: "Sai", fileName: "vcnv-incorrect" },
                                { displayName: "Mở mảnh ghép", fileName: "vcnv-open" },
                                { displayName: "Đúng CNV", fileName: "vcnv-bellcorrect" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "tangtoc"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Giới thiệu", fileName: "tangtoc-start" },
                                { displayName: "10s", fileName: "tangtoc-10secs" },
                                { displayName: "20s", fileName: "tangtoc-20secs" },
                                { displayName: "30s", fileName: "tangtoc-30secs" },
                                { displayName: "40s", fileName: "tangtoc-40secs" },
                                { displayName: "Đáp án", fileName: "tangtoc-showanswers" },
                                { displayName: "Đúng", fileName: "tangtoc-correct" },
                                { displayName: "Sai", fileName: "tangtoc-wrong" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "vedich"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Giới thiệu", fileName: "vedich-start" },
                                { displayName: "Bước lên", fileName: "vedich-onstage" },
                                { displayName: "Chọn", fileName: "vedich-packagechoice" },
                                { displayName: "Xác nhận", fileName: "vedich-confirmchoice" },
                                { displayName: "15s", fileName: "vedich-15secs" },
                                { displayName: "20s", fileName: "vedich-20secs" },
                                { displayName: "Hy vọng", fileName: "vedich-star" },
                                { displayName: "Cơ hội", fileName: "vedich-poll" },
                                { displayName: "Chuông", fileName: "vedich-bell" },
                                { displayName: "Đúng", fileName: "vedich-correct" },
                                { displayName: "Hoàn thành", fileName: "vedich-complete" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "tiebreaker"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Sẵn sàng", fileName: "khoidong-ready" },
                                { displayName: "Nhạc nền", fileName: "khoidong-bgm" },
                                { displayName: "Đúng", fileName: "khoidong-correct" },
                                { displayName: "Sai", fileName: "khoidong-incorrect" },
                                { displayName: "Chuông", fileName: "khoidong-bell" },
                                { displayName: "Hoàn thành", fileName: "khoidong-complete" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "tkd"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Tổng kết nhanh", fileName: "common-scoresum" },
                                { displayName: "#4", fileName: "tongket-4th" },
                                { displayName: "#3", fileName: "tongket-3rd" },
                                { displayName: "#2", fileName: "tongket-2nd" },
                                { displayName: "#1", fileName: "tongket-1st" }
                            ]}
                        />
                    {:else if $states.available_parts[$states.current_part] == "standby"}
                        <SoundBoard
                            {gm}
                            sounds={[
                                { displayName: "Nhạc MC", fileName: "op-introduction" },
                                { displayName: "GT thí sinh", fileName: "op-introducecontestants" },
                                { displayName: "Trao giải", fileName: "tongket-award" }
                            ]}
                        />
                    {/if}
                    <!-- <ScoreJudge {conn} {states} {gm} /> -->
                </div>
            </div>
        </div>
    </Load>
</div>
<!-- Prevents spacebar from triggering recently pressed button -->
<svelte:window on:keyup|preventDefault={() => {}} on:keypress|preventDefault={() => {}} />

<style>
    .container {
        display: flex;
        flex-direction: column;
        gap: 25px;
        width: fit-content;
    }

    .bg {
        position: fixed;
        width: 100%;
        height: 100%;
        overflow: hidden;
        background: var(--bg-dark-1);
        padding: 2em;
    }

    .right {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    .horizontal {
        display: grid;
        grid-template-columns: 50vw 50vw;
        flex-direction: row;
        gap: 15px;
    }
</style>
