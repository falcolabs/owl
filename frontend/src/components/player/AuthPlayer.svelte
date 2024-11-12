<script lang="ts">
    import { GameMaster, SHOW_NAME, ORG_NAME } from "$lib";
    import { writable } from "svelte/store";
    import { onMount } from "svelte";
    import TitleBar from "../TitleBar.svelte";

    let username = "";
    let accessKey = "";
    export let gm: GameMaster;
    let authenticated = writable(false);

    onMount(async () => {
        authenticated = gm.isAuthenticated;
    });

    const click = async () => {
        await gm.authenticate(username, accessKey);
    };
</script>

<title>Authentication - {SHOW_NAME}</title>
<div class="bg">
    <TitleBar activity="Ủy quyền dự thi" />
    <div class="center">
        <div class="box">
            <form on:submit|preventDefault={async () => {}}>
                <h1 class="prompt plabel">Ủy quyền dự thi</h1>

                <div class="pillcon">
                    {#if $authenticated}
                        <div class="confspot">Đã được ủy quyền.<br />Phần thi sẽ sớm bắt đầu.</div>
                    {:else}
                        <div class="inpgroup">
                            <p class="tag">Mã thí sinh</p>
                            <input type="text" class="inp" bind:value={username} />
                        </div>
                        <div class="inpgroup">
                            <p class="tag">Khóa truy cập</p>
                            <input type="password" class="inp" bind:value={accessKey} />
                        </div>
                        <button class="pill confspot" on:click={click}>Bắt đầu</button>
                    {/if}
                    <p class="cpy">
                        Ⓒ 2024 {ORG_NAME}. Đây là phần mềm nguồn mở, phát hành theo giấy phép GPL3.
                    </p>
                </div>
            </form>
        </div>
    </div>
</div>

<style>
    .cpy {
        font-size: 16px;
        text-align: center;
        color: #888ebf;
        margin-bottom: -30px;
        width: 30rem;
    }

    .pill {
        cursor: pointer;
        transition: 100ms ease-in;
    }

    .pill:hover {
        filter: brightness(90%);
    }

    .pill:active {
        filter: brightness(80%);
    }

    .pillcon {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: fit-content;
    }

    .confspot {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        color: #fff;
        padding: 15px 50px;
        margin-top: 20px;
        margin-bottom: 60px;
        line-height: 1.2;
    }

    .plabel {
        margin-bottom: 50px;
    }

    .tag {
        margin-bottom: 10px;
    }

    .inpgroup {
        width: 100%;
        margin-bottom: 25px;
    }

    .inp {
        width: 570px;
    }

    .box {
        padding: 50px 100px;
        margin-top: 50px;
    }

    .bg {
        width: 100vw;
        height: 100vh;
        overflow: hidden;
        background: var(--bg-gradient);
    }

    .center {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100vw;
        height: 100%;
    }
</style>
