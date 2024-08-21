import { Peeker, Connection } from "$lib";
import type { PacketType, Packet, PortableType, GameState, Timer } from "client";

export type AcceptableValue = any[] | number | string | boolean | null | object;

export class StateManager {
    state_storage!: Map<string, GameState>
    connection!: Connection
    listeners!: Map<string, (value: GameState) => void>
    state!: { [key: string]: AcceptableValue }
    listen_all!: (state: { [key: string]: AcceptableValue }) => void

    private handleState(state: GameState) {
        this.state_storage.set(state.name, state);
        this.listeners.forEach((handle, name) => {
            if (state.name == name) {
                handle(state);
            }
        });
        this.state[state.name] = JSON.parse(state.data.data);
        this.listen_all(this.state);
    }

    static async create(connection: Connection): Promise<StateManager> {
        let obj = new StateManager();
        obj.connection = connection;
        obj.state_storage = new Map();
        obj.listeners = new Map();
        obj.state = { __init: false }
        obj.listen_all = (_) => { }
        connection.on(Peeker.PacketType.StateList, (packet) => {
            packet.value.forEach((state) => {
                obj.handleState(state)
            })
            obj.state.__init = true
        })
        connection.on(Peeker.PacketType.State, (packet) => {
            obj.handleState(packet.value)

        })
        await obj.updateAll();
        return obj
    }

    isInitialized(): boolean {
        // @ts-ignore
        return this.state.__init
    }

    get timer(): Timer {
        if (this.state.timer_json === undefined) {
            return new Peeker.Timer();
        }
        // @ts-ignore
        return Peeker.Timer.from(this.state.timer_json);
    }

    async updateAll() {
        await this.connection.send(Peeker.Query.stateList());
    }

    on_change(handle: (state: { [key: string]: AcceptableValue }) => void) {
        this.listen_all = handle;
    }

    on_state(name: string, handle: (value: GameState) => void) {
        this.listeners.set(name, handle);
    }

    on_value(name: string, handle: (value: AcceptableValue) => void) {
        this.listeners.set(name, (gameState) => {
            handle(JSON.parse(gameState.data.data))
        })
    }

    get(name: string): GameState {
        let ret = this.state_storage.get(name);
        if (ret === undefined) {
            throw new Error(`GameState ${name} not found.`);
        }
        return ret;
    }

    get_value(name: string): AcceptableValue {
        let ret = this.state_storage.get(name);
        if (ret === undefined) {
            throw new Error(`GameState ${name} not found.`);
        }
        return JSON.parse(ret.data.data);
    }

    async setArray(name: string, t: any[]) {
        this.connection.send(UpdateState.create(name, t, Peeker.PortableType.ARRAY));
    }

    async setNumber(name: string, t: number) {
        this.connection.send(UpdateState.create(name, t, Peeker.PortableType.NUMBER));
    }

    async setString(name: string, t: string) {
        this.connection.send(UpdateState.create(name, t, Peeker.PortableType.STRING));
    }

    async setNull(name: string) {
        this.connection.send(UpdateState.create(name, null, Peeker.PortableType.NULL));
    }

    async setObject(name: string, t: object) {
        this.connection.send(UpdateState.create(name, t, Peeker.PortableType.OBJECT));
    }

    // async setTimer(t: Timer) {
    //     this.connection.send(UpdateState.create("timer_json", t.pack(), Peeker.PortableType.STRING));
    // }

}


export class UpdateState {
    static create(name: string, value: AcceptableValue, type: PortableType): Packet<PacketType.UpdateState> {
        return new Peeker.Packet(
            Peeker.PacketType.UpdateState,
            {
                name: name,
                data: {
                    data: JSON.stringify(value),
                    dataType: type
                },
            }
        )
    }

    static array(name: string, t: any[]): Packet<PacketType.UpdateState> {
        return UpdateState.create(name, t, Peeker.PortableType.ARRAY)
    }

    static number(name: string, t: number): Packet<PacketType.UpdateState> {
        return UpdateState.create(name, t, Peeker.PortableType.NUMBER)
    }

    static string(name: string, t: string): Packet<PacketType.UpdateState> {
        return UpdateState.create(name, t, Peeker.PortableType.STRING)
    }

    static null(name: string): Packet<PacketType.UpdateState> {
        return UpdateState.create(name, null, Peeker.PortableType.NULL)
    }

    static object(name: string, t: object): Packet<PacketType.UpdateState> {
        return UpdateState.create(name, t, Peeker.PortableType.OBJECT)
    }
}