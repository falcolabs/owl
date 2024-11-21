import { Connection, Peeker } from "$lib";
import type { Player } from "client";
import type { Readable, Unsubscriber } from "svelte/store";


export class PlayerManager implements Readable<Map<string, Player>> {
    connection!: Connection;
    public storage!: Map<string, Player>;
    updateListeners!: ((players: Map<string, Player>) => void)[]

    static async create(connection: Connection): Promise<PlayerManager> {
        let obj = new PlayerManager();
        obj.connection = connection;
        obj.storage = new Map();
        obj.updateListeners = []
        connection.on(Peeker.PacketType.PlayerList, (packet) => {
            packet.value.forEach((p) => {
                obj.storage.set(p.identifier, p)
            });
            obj.updateListeners.forEach((cb) => cb(obj.storage))
        })
        connection.on(Peeker.PacketType.Player, (packet) => {
            obj.storage.set(packet.value.identifier, packet.value);
            obj.updateListeners.forEach((cb) => cb(obj.storage))
        })
        return obj
    }

    static getDisplayName(identifier: string, pl: any[]): string {
        for (let p of pl) {
            if (p.identifier == identifier) {
                return p.name;
            }
        }
        throw new Error(`Cannot find player with username ${identifier}`)
    }

    get list(): Player[] {
        return Array.from(this.storage.values());
    }

    subscribe(handle: (players: Map<string, Player>) => void): Unsubscriber {
        handle(this.storage);
        let len = this.updateListeners.push(handle);
        return () => { this.unsubscribe(len - 1) };
    }

    unsubscribe(index: number) {
        this.updateListeners.splice(index, 1);
    }

    name(identifier: string): Player {
        // TODO - make this | undefined
        // @ts-ignore
        return this.storage.get(identifier);
    }

    async updateAll() {
        await this.connection.send(Peeker.Query.playerList());
    }
}
