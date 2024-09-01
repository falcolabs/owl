import type { Timer, GameState } from "client";
import { Connection, Peeker, type AcceptableValue } from "$lib";
import { Push } from "$lib/push";
import { readable, writable, type Readable, type Unsubscriber, type Writable } from "svelte/store";

export class StateManager implements Readable<any> {
    raw_states!: Map<string, GameState>
    connection!: Connection
    listeners!: Map<string, (value: GameState) => void>
    updateListeners!: ((state: { [key: string]: AcceptableValue }) => void)[]
    timerStore!: Writable<Timer>

    public store!: any /* { [key: string]: AcceptableValue }*/

    static async create(connection: Connection): Promise<StateManager> {
        let obj = new StateManager();

        obj.store = { __init: false }
        obj.connection = connection;
        obj.raw_states = new Map();
        obj.listeners = new Map();
        obj.updateListeners = []

        let def;
        if (obj.store.timer_json === undefined) {
            def = new Peeker.Timer();
        } else {
            def = Peeker.Timer.from(obj.store.timer_json);
        }
        obj.timerStore = writable(def);

        connection.on(Peeker.PacketType.StateList, (packet) => {
            packet.value.forEach((state) => {
                obj.handleState(state)
            })
            obj.store.__init = true
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
        if (state.name == "timer_json") {
            this.timerStore.set(Peeker.Timer.from(this.store.timer_json))
        }
    }


    async updateAll() {
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

    async setTimer(t: Timer) {
        await this.connection.send(Push.create("timer_json", t.pack(), Peeker.PortableType.OBJECT));
    }
}
