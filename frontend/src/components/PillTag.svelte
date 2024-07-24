<script lang="ts">
    export let text: string;
</script>

<div class="pill pilltag">
    <div class="text">{text}</div>
    <div class="decor">
        <svg class="ball" viewBox="0 0 80 80">
            <circle cx="40" cy="40" r="40" fill="url(#ball)" />
            <defs>
                <linearGradient
                    id="ball"
                    x1="73.8286"
                    y1="8.68572"
                    x2="40"
                    y2="40"
                    gradientUnits="userSpaceOnUse"
                >
                    <stop stop-color="#ABC6FA" stop-opacity="0.72" />
                    <stop offset="1" stop-color="#D9D9D9" stop-opacity="0" />
                </linearGradient>
            </defs>
        </svg>
        <svg class="ball" viewBox="0 0 81 81">
            <circle
                cx="40.692"
                cy="40.692"
                r="40"
                transform="rotate(-89 40.692 40.692)"
                fill="url(#ball2)"
            />
            <defs>
                <linearGradient
                    id="ball2"
                    x1="74.5206"
                    y1="9.37773"
                    x2="40.692"
                    y2="40.692"
                    gradientUnits="userSpaceOnUse"
                >
                    <stop stop-color="#ABC6FA" stop-opacity="0.72" />
                    <stop offset="1" stop-color="#D9D9D9" stop-opacity="0" />
                </linearGradient>
            </defs>
        </svg>
    </div>
</div>

<style>
    .text {
        position: absolute;
        font-weight: bold;
        z-index: 6;
    }

    .ball {
        flex-grow: 0;
        height: 2em;
        width: auto;
    }

    .decor {
        width: 100%;
        z-index: 5;
        display: flex;
        flex-direction: row;
        transform: translateY(10px);
        justify-content: space-between;
    }

    .pilltag {
        position: absolute;
        transform: translateY(-3em);
        overflow: hidden;
        font-size: 1.5em;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        /* padding: 16px 100px; */
        width: 325px;
        height: 70px;
        box-shadow: 0 4px 4px 0 #00000040;
    }
</style>
