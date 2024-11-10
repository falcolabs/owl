<script lang="ts">
    import VcnvLine from "./VCNVLine.svelte";
    import PillTag from "../PillTag.svelte";
    import type { StateManager } from "$lib";
    import { writable, type Readable, type Writable } from "svelte/store";
    import TimerBar from "../TimerBar.svelte";
    export let states: StateManager;

    let lines = writable(
        new Map<string, Writable<{ status: string; content: string; tag: string }>>()
    );
    states.subscribe((s) => {
        if (s.puzzle_data == undefined) return;
        if (s.final_hint) {
            if ($lines.size != 1) {
                console.log("M");
                let o = new Map();
                o.set(s.puzzle_data.center.tag, writable(s.puzzle_data.center));
                lines.set(o);
            } else {
                $lines.get(s.puzzle_data.center.tag)?.set(s.puzzle_data.center);
            }
        } else {
            if ($lines.size != 4) {
                let o = new Map();
                for (let entry of $states.puzzle_data.normal) {
                    o.set(entry.tag, writable(entry));
                }
                lines.set(o);
            } else {
                for (let entry of $states.puzzle_data.normal) {
                    $lines.get(entry.tag)?.set(entry);
                }
            }
        }
    });
</script>

<div class="top">
    <div class="left">
        <div class="up box">
            {#each $lines as [_, line]}
                <VcnvLine {line} />
            {/each}
        </div>
        <div class="qbox box">
            <div class="ptag">
                <PillTag text={$states.selected != "" ? "Hàng 1" : "Lựa chọn"} />
            </div>
            <p class="prompt">{$states.prompt}</p>
            <div class="timerbar"><TimerBar {states} /></div>
        </div>
    </div>
    <div class="picontainer">
        <div class="annc">CHƯỚNG NGẠI VẬT CÓ {$states.key_length} CHỮ CÁI</div>
        <img src="data:image/webp;base64, {$states.image}" class="picture" alt="" />
    </div>
</div>

<style>
    .box {
        padding: 40px;
    }

    .annc {
        width: 100%;
        height: 60px;
        background-color: var(--accent);
        border-radius: var(--radius-1);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: var(--shadow-s);
        font-weight: bold;
    }

    .top {
        display: flex;
        flex-direction: row;
        gap: 60px;
        transform: translateY(-1.5rem);
    }

    .qbox {
        width: 40vw;
        height: 100%;
        min-height: 12rem;
        display: flex;
        justify-content: space-between;
        flex-direction: column;
    }

    .picontainer {
        display: flex;
        flex-direction: column;
        gap: 20px;
        width: max-content;
        width: 40vw;
    }

    .timerbar {
        margin-top: 2rem;
        margin-bottom: -15px;
    }

    .picture {
        object-fit: cover;
        box-shadow: 7px 10px 33px 3px #00000040;
        height: 100%;

        border-radius: var(--radius-1);
        overflow: hidden;
    }

    .left {
        display: flex;
        flex-direction: column;
        gap: 60px;
    }

    .up {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .ptag {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        width: inherit;
        height: 60px;
        transform: translateY(-4.5rem);
    }
</style>
