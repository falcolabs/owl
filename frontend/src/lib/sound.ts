import { Connection, Peeker } from "$lib";
import { openDB, deleteDB, wrap, unwrap, type IDBPDatabase, type IDBPObjectStore } from 'idb';

export class SoundManager {
    connection!: Connection;
    db!: IDBPDatabase;
    soundStore!: IDBPObjectStore;

    static async create(conn: Connection) {
        let obj = new SoundManager();
        obj.connection = conn;

        const db = await openDB("owlSound", 1, {
            upgrade(db) {
                {
                    db.createObjectStore("sounds", { keyPath: "ident" })

                }
            },
        });

        conn.on(Peeker.PacketType.PlaySound, async (psp) => {
            await new Audio(URL.createObjectURL(await db.get("sounds", psp.value))).play()
        })

        if (window.localStorage.getItem("owlSoundDownloaded") != "true") {
            let ctl = await fetch("/sounds/catalog.json");

            Object.values(await ctl.json()).forEach(async (v: any) => {
                try {
                    console.log("Downloading", v.fileName)

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

        return obj;
    }
}
