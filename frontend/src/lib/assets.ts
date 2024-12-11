import type { StateManager } from "$lib/state";
import { openDB, type IDBPDatabase } from 'idb';

export class AssetManager {
    db!: IDBPDatabase;

    static async create(states: StateManager): Promise<AssetManager> {
        let obj = new AssetManager();
        const db = await openDB("owlAssets", 1, {
            upgrade(db) {
                {
                    db.createObjectStore("assets", { keyPath: "url" })

                }
            },
        });
        obj.db = db;
        if (window.localStorage.getItem("owlAssetsReady") != "true") {
            states.onready(async (s) => {
                // @ts-ignore
                s.engine_assets.forEach(async (url: string) => {
                    let res = await fetch(url);
                    await db.add("assets", {
                        url: url,
                        blob: await res.blob()
                    })
                });
                window.localStorage.setItem("owlAssetsReady", "true");
            })
        }

        return obj;
    }

    async getURL(url: string): Promise<string> {
        return URL.createObjectURL((await this.db.get("assets", url)).blob);
    }
}
