<script lang="ts">
    import ScorePill from "./ScorePill.svelte";
    const PLAYER_DATA: [string, { score: number; activated: boolean }][] = Object.entries({
        "Imap Ussay": { score: 20, activated: true },
        "Hugh Jazz": { score: 20, activated: false },
        "Quang Liêm": { score: 20, activated: false },
        "Quang Trung": { score: 20, activated: false }
    });
</script>

<div class="bar">
    {#each PLAYER_DATA as [name, { activated, score }]}
        <ScorePill {activated} {name} {score} />
    {/each}
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
</style>
