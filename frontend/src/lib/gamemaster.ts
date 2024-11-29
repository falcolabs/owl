import { Peeker, Connection, CallProcedure } from "$lib";
import type { AvailableSound } from "client";
import { PlayerManager } from "$lib/player";
import { StateManager } from "$lib/state";
import { writable, type Writable } from "svelte/store";

export type AcceptableValue = any[] | number | string | boolean | null | object;

export class GameMaster {
    connection!: Connection;
    updateListeners!: ((gm: GameMaster) => void)[];

    public states!: StateManager;
    public players!: PlayerManager;

    public partName!: Writable<string>;
    public isAuthenticated!: Writable<boolean>;
    public authToken!: string;
    public username: string = "";

    static async create(connection: Connection): Promise<GameMaster> {
        let obj = new GameMaster();
        obj.states = await StateManager.create(connection);
        obj.players = await PlayerManager.create(connection);
        obj.connection = connection;
        obj.isAuthenticated = writable(false);
        obj.partName = writable("");
        obj.connection.on(Peeker.PacketType.Part, (packetPart) => {
            obj.partName.set(packetPart.value.name);
        });

        obj.states.onready = async (_) => {
            let ad = window.sessionStorage.getItem("authData");
            if (ad !== null && ad !== "") {
                let adt = JSON.parse(ad);
                obj.username = adt.username;
                await connection.send(
                    new Peeker.Packet(Peeker.PacketType.CommenceSession, {
                        username: adt.username,
                        accessKey: adt.accessKey,
                    })
                );
            }
        };

        obj.connection.on(Peeker.PacketType.AuthStatus, (packet) => {
            if (packet.value.success) {
                obj.authToken = packet.value.token;
                obj.isAuthenticated.set(true);
            }
        });

        await obj.updateAll();
        return obj;
    }

    isInitialized(): boolean {
        // @ts-ignore
        return this.states.__init;
    }

    async authenticate(username: string, accessKey: string) {
        this.username = username;
        window.sessionStorage.setItem(
            "authData",
            JSON.stringify({
                username: username,
                accessKey: accessKey,
            })
        );
        await this.connection.send(
            new Peeker.Packet(Peeker.PacketType.CommenceSession, {
                username: username,
                accessKey: accessKey,
            })
        );
    }

    async play_sound(sound_name: AvailableSound) {
        await this.connection.send(CallProcedure.name("engine::play_sound").string("soundName", sound_name).build());
    }

    async timer_operation(operation: "start" | "pause" | "reset") {
        await this.connection.send(CallProcedure.name("engine::timer_operation").string("operation", operation).build());
    }

    async updateAll() {
        await this.states.updateAll();
        await this.players.updateAll();
        await this.connection.send(Peeker.Query.currentPart());
    }
}
