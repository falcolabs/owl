import { Connection } from "$lib";

export class SoundManager {
    connection!: Connection;
    db!: IDBDatabase;

    static async create(conn: Connection) {
        let obj = new SoundManager();
        obj.connection = conn;

        let a = window.indexedDB.open("owlSound");
        // @ts-ignore
        a.onsuccess((_) => {
            obj.db = a.result;
        });

        fetch("/sounds/catalog.json");
    }
}
