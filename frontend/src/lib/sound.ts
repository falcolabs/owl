import { GameMaster, Peeker, StateManager } from "$lib";
import { openDB, type IDBPDatabase, type IDBPObjectStore } from 'idb';
import { writable, type Writable } from "svelte/store";
import type { AvailableSound, Packet, PacketType } from "client";

export class SoundManager {
    gm!: GameMaster;
    states!: StateManager;
    db!: IDBPDatabase;
    soundStore!: IDBPObjectStore;
    downloadText!: Writable<string>;
    onready!: (db: IDBPDatabase) => void;
    isReady!: boolean;
    soundHandles!: Map<AvailableSound, HTMLAudioElement>
    subscribe_onplay!: ((sound: AvailableSound) => void)[]
    subscribe_onstop!: ((sound: AvailableSound) => void)[]


    static async create(gm: GameMaster) {
        let obj = new SoundManager();
        obj.gm = gm;
        obj.downloadText = writable("")
        obj.onready = (_) => { }
        obj.isReady = false
        obj.soundHandles = new Map();
        obj.subscribe_onplay = []
        obj.subscribe_onstop = []

        const db = await openDB("owlSounds", 1, {
            upgrade(db) {
                {
                    db.createObjectStore("sounds", { keyPath: "ident" })

                }
            },
        });
        obj.db = db;

        gm.connection.on(Peeker.PacketType.PlaySound, async (psp: Packet<PacketType.PlaySound>) => {
            // @ts-ignore
            await obj.play(psp.value);
        })
        gm.states.on("active_sounds", async (data: any) => {
            obj.soundHandles.forEach((handle, sn) => {
                if (!data.includes(sn)) {
                    handle.pause();
                    handle.remove();
                    obj.soundHandles.delete(sn);
                    obj.subscribe_onstop.forEach((f) => f(sn))
                }
            })
        }
        )

        if (window.localStorage.getItem("owlSoundDownloaded") != "true") {
            console.log(`Fetching sound catalog`)
            obj.downloadText.set(`Fetching sound catalog`)
            let ctl = await fetch("/sounds/catalog.json");

            Object.values(await ctl.json()).forEach(async (v: any) => {
                try {
                    obj.downloadText.set(`Downloading ${v.fileName}`)
                    console.log(`Downloading ${v.fileName}`)

                    let res = await fetch(`/sounds/${v.fileName}.webm`)
                    await db.add("sounds", {
                        ident: v.fileName,
                        blob: await res.blob()
                    })
                } catch (e) {

                }
            })
        }
        window.localStorage.setItem("owlSoundDownloaded", "true");
        obj.downloadText.set(`Download complete.`)
        obj.isReady = true
        obj.onready(obj.db);
        return obj;
    }

    subscribe(on: "play" | "stop", callback: (sound_name: AvailableSound) => void) {
        if (on === "play") {
            this.subscribe_onplay.push(callback);
        } else if (on === "stop") {
            this.subscribe_onstop.push(callback);
        } else {
            throw new Error(`on cannot be any other value than "play" or "stop" (provided ${on}).`)
        }
    }

    async play(sound_name: AvailableSound) {
        if (this.soundHandles.has(sound_name)) {
            let el = this.soundHandles.get(sound_name);
            el?.pause();
            el?.remove();
            this.soundHandles.delete(sound_name);
            this.subscribe_onstop.forEach((f) => f(sound_name))
        }
        let ae = new Audio(URL.createObjectURL((await this.db.get("sounds", sound_name)).blob))
        this.soundHandles.set(sound_name, ae);
        ae.onended = async (_) => {
            await this.gm.sound.stop(sound_name);
        }
        this.subscribe_onplay.forEach((f) => f(sound_name))
        try {
            await ae.play();
        } catch (e) {
            console.log(e)
        }
    }
}
