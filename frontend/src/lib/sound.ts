import { CallProcedure, Connection, Peeker } from "$lib";
import { openDB, type IDBPDatabase, type IDBPObjectStore } from 'idb';
import { writable, type Writable } from "svelte/store";
import type { AvailableSound } from "client";

export class SoundManager {
    connection!: Connection;
    db!: IDBPDatabase;
    soundStore!: IDBPObjectStore;
    downloadText!: Writable<string>;
    onready!: (db: IDBPDatabase) => void;
    isReady!: boolean;

    static async create(conn: Connection) {
        let obj = new SoundManager();
        obj.connection = conn;
        obj.downloadText = writable("")
        obj.onready = (_) => { }
        obj.isReady = false

        const db = await openDB("owlSound", 1, {
            upgrade(db) {
                {
                    db.createObjectStore("sounds", { keyPath: "ident" })

                }
            },
        });
        obj.db = db;

        conn.on(Peeker.PacketType.PlaySound, async (psp) => {
            await new Audio(URL.createObjectURL((await db.get("sounds", psp.value)).blob)).play()
        })

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
        console.log(`Download complete.`)
        obj.isReady = true
        obj.onready(obj.db);
        return obj;
    }

    async play(sound_name: AvailableSound) {
        await new Audio(URL.createObjectURL((await this.db.get("sounds", sound_name)).blob)).play()
    }
}
