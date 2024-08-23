import { Peeker, Connection } from "$lib";
import { PlayerManager } from "$lib/player";
import { StateManager } from "$lib/state"
import type { Invalidator, Readable, Subscriber, Unsubscriber } from "svelte/store";

export type AcceptableValue = any[] | number | string | boolean | null | object;

export class GameMaster {
    connection!: Connection
    updateListeners!: ((gm: GameMaster) => void)[]

    public states!: StateManager;
    public players!: PlayerManager;

    static async create(connection: Connection): Promise<GameMaster> {
        let obj = new GameMaster();
        obj.states = await StateManager.create(connection);
        obj.players = await PlayerManager.create(connection);
        obj.connection = connection;
        await obj.updateAll()
        return obj
    }

    isInitialized(): boolean {
        // @ts-ignore
        return this.states.__init
    }

    async updateAll() {
        await this.states.updateAll();
        await this.players.updateAll()
    }

}
