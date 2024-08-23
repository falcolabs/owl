<script lang="ts">
    // import { getPeeker } from "$lib";
    import { SHOW_NAME, ORG_NAME, Peeker, Connection } from "$lib";
    import { PacketType, type Packet } from "client";
    import { onMount } from "svelte";
    import TitleBar from "../components/TitleBar.svelte";
    import { goto } from "$app/navigation";
    
    let username: HTMLInputElement;
    let accessKey: HTMLInputElement;
    let conn: Connection;
    let unavailable: boolean = false;
    let authenticated: boolean = false;
    onMount(async () => {
        conn = await Connection.create();
        if (conn.currentPart != "auth") {
            unavailable = true;
        }
        conn.on(PacketType.AuthStatus, (packet) => {
            if (packet.value.success) {
                //     console.log("redirecting");
                //     goto(`/game/khoidong?token=${packet.value.token}`).then(() => {
                //         console.error("Failed to redirect to target.");
                //     });
                authenticated = true;
            }
        });
    });

    const click = async () => {
        await conn.send(
            new Peeker.Packet(Peeker.PacketType.CommenceSession, {
                username: username.value,
                accessKey: accessKey.value
            })
        );
    };
</script>

<title>Authentication - {SHOW_NAME}</title>
<div class="bg">
    {#if !unavailable}
        <TitleBar activity="Ủy quyền dự thi" />
        <div class="center">
            <div class="box">
                <h1 class="prompt plabel">Ủy quyền dự thi</h1>
                <div class="inpgroup">
                    <p class="tag">Mã thí sinh</p>
                    <input type="text" class="inp" bind:this={username} />
                </div>
                <div class="inpgroup">
                    <p class="tag">Khóa truy cập</p>
                    <input type="password" class="inp" bind:this={accessKey} />
                </div>
                <div class="pillcon">
                    {#if authenticated}
                        <div class="confspot">Đã được ủy quyền.<br />Phần thi sẽ sớm bắt đầu.</div>
                    {:else}
                        <button class="pill confspot" on:click={click}>Bắt đầu</button>
                    {/if}
                    <p class="cpy">
                        Ⓒ 2024 {ORG_NAME}. Đây là phần mềm nguồn mở, phát hành theo giấy phép GPL3.
                    </p>
                </div>
            </div>
        </div>
    {:else}
        <h1 class="prompt plabel">
            Đã hết thời gian ủy quyền. Nếu bạn là thí sinh<br />mà gặp phải màn hình này, hãy liên
            hệ ban tổ chức.
        </h1>
    {/if}
</div>

<style>
    .cpy {
        font-size: 16px;
        text-align: center;
        color: #888ebf;
        margin-bottom: -30px;
        width: 30rem;
    }

    .inp {
        transition: 100ms ease-in;
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
