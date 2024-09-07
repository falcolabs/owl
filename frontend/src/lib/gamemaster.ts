import { Peeker, Connection } from "$lib";
import { PlayerManager } from "$lib/player";
import { StateManager } from "$lib/state"
import { writable, type Writable } from "svelte/store";

export type AcceptableValue = any[] | number | string | boolean | null | object;

export class GameMaster {
    connection!: Connection
    updateListeners!: ((gm: GameMaster) => void)[]

    public states!: StateManager;
    public players!: PlayerManager;
    public partName!: Writable<string>;

    static async create(connection: Connection): Promise<GameMaster> {
        let obj = new GameMaster();
        obj.states = await StateManager.create(connection);
        obj.players = await PlayerManager.create(connection);
        obj.connection = connection;
        obj.partName = writable("");
        obj.connection.on(Peeker.PacketType.Part, (packetPart) => {
            obj.partName.set(packetPart.value.name);
        })
        await obj.updateAll()
        return obj
    }

    isInitialized(): boolean {
        // @ts-ignore
        return this.states.__init
    }

    async updateAll() {
        await this.states.updateAll();
        await this.players.updateAll();
        await this.connection.send(Peeker.Query.currentPart());
    }

}
