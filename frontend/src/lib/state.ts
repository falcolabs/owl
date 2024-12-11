import type { Timer, GameState } from "client";
import { Connection, Peeker, type AcceptableValue } from "$lib";
import { Push } from "$lib/push";
import { readable, writable, type Readable, type Unsubscriber, type Writable } from "svelte/store";

export class StateManager implements Readable<any> {
    raw_states!: Map<string, GameState>
    connection!: Connection
    wstime!: WebSocket
    listeners!: Map<string, (value: GameState) => void>
    updateListeners!: ((state: { [key: string]: AcceptableValue }) => void)[]
    time!: Writable<number>;
    onReadyList!: ((store: { [key: string]: AcceptableValue }) => void)[];
    public store!: any /* { [key: string]: AcceptableValue }*/

    static async create(connection: Connection): Promise<StateManager> {
        let obj = new StateManager();

        obj.store = { __init: false }
        obj.connection = connection;
        obj.raw_states = new Map();
        obj.listeners = new Map();
        obj.updateListeners = []
        obj.wstime = new WebSocket(`ws://${import.meta.env.VITE_WSENDPOINT}/time`);
        obj.onReadyList = []
        obj.time = writable(0);
        obj.wstime.onmessage = ((me) => {
            let time = JSON.parse(me.data);
            obj.time.set(time)
        });

        connection.on(Peeker.PacketType.StateList, (packet) => {
            packet.value.forEach((state) => {
                obj.handleState(state)
            })
            obj.store.__init = true
            obj.onReadyList.forEach(cb => cb(obj.store));
            obj.updateListeners.forEach((cb) => cb(obj.store));
        })

        connection.on(Peeker.PacketType.State, (packet) => {
            obj.handleState(packet.value)
            obj.updateListeners.forEach((cb) => cb(obj.store));
        })
        return obj;
    }

    private handleState(state: GameState) {
        this.raw_states.set(state.name, state);
        this.listeners.forEach((handle, name) => {
            if (state.name == name) {
                handle(state);
            }
        });
        this.store[state.name] = JSON.parse(state.data.data);
    }

    isInitialized(): boolean {
        return this.store.__init;
    }

    flush() {
        this.store = { __init: false };
    }

    onready(cb: (store: { [key: string]: AcceptableValue }) => void) {
        this.onReadyList.push(cb);
        if (this.store.__init) {
            cb(this.store);
        }
    }

    async updateAll() {
        this.flush()
        await this.connection.send(Peeker.Query.stateList());
    }

    subscribe(handle: (state: { [key: string]: any /* AcceptableValue */ }) => void): Unsubscriber {
        handle(this.store);
        let len = this.updateListeners.push(handle);
        return () => { this.unsubscribe(len - 1) };
    }

    unsubscribe(index: number) {
        this.updateListeners.splice(index, 1);
    }

    on_state(name: string, handle: (value: GameState) => void) {
        this.listeners.set(name, handle);
    }

    on(name: string, handle: (value: AcceptableValue) => void) {
        this.listeners.set(name, (gameState) => {
            handle(JSON.parse(gameState.data.data))
        })
    }

    get_state(name: string): GameState {
        let ret = this.raw_states.get(name);
        if (ret === undefined) {
            throw new Error(`GameState ${name} not found.`);
        }
        return ret;
    }

    get(name: string): AcceptableValue {
        let ret = this.store[name];
        if (ret === undefined) {
            throw new Error(`GameState ${name} not found.`);
        }
        return ret;
    }

    async setArray(name: string, t: any[]) {
        await this.connection.send(Push.array(name, t));
    }

    async setNumber(name: string, t: number) {
        await this.connection.send(Push.number(name, t));
    }

    async setString(name: string, t: string) {
        await this.connection.send(Push.string(name, t));
    }

    async setNull(name: string) {
        await this.connection.send(Push.null(name));
    }

    async setObject(name: string, t: object) {
        await this.connection.send(Push.object(name, t));
    }

    async setBoolean(name: string, t: boolean) {
        await this.connection.send(Push.boolean(name, t));
    }
}
