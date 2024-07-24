<script lang="ts">
    // import { getPeeker } from "$lib";
    import { SHOW_NAME, ORG_NAME } from "$lib";
    import { onMount } from "svelte";
    import TitleBar from "../components/TitleBar.svelte";
    import { redirect } from "@sveltejs/kit";

    let peeker: typeof import("client");
    let ctx: import("client").Context;
    let res: string;
    let username: HTMLInputElement;
    let accessKey: HTMLInputElement;
    let auth: import("client").Auth;
    onMount(async () => {
        peeker = await import("client");
        peeker.panic_bait();
        auth = new peeker.Auth((success: boolean) => {
            console.log("yes. 3 days of work: ", success);
            redirect(303, `/game/khoidong?uuid=${username.value}`);
        });
        ctx = await peeker.Context.create((pname: string) => {
            if (pname == "auth") return auth;
        });
        console.log(ctx);
    });

    const click = async () => {
        console.log("hi");
        auth.login(ctx, username.value, accessKey.value);
    };
</script>

<title>Authentication - {SHOW_NAME}</title>
<div class="bg">
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
                <button class="pill" on:click={click}>Bắt đầu</button>
                <p class="cpy">
                    Ⓒ 2024 {ORG_NAME}. Đây là phần mềm nguồn mở, phát hành theo giấy phép GPL3.
                </p>
            </div>
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

    .pillcon {
        width: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: fit-content;
    }

    .pill {
        font-size: 1.5rem;
        font-weight: bold;
        text-align: center;
        color: #fff;
        padding: 15px 50px;
        margin-bottom: 60px;
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
