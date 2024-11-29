// place files you want to import through the `$lib` alias in this folder.

export const ORG_NAME: string = "Đoàn trường THPT Chuyên Bắc Ninh · THPT Chuyên Bắc Ninh";
export const SHOW_NAME: string = "Đường Đua Xanh";
export const SUBTEXT: string = "Mùa 5, Bán kết 1"

import type { PacketType, Packet, _PacketValue, _PacketVariant } from "client";
type CBHandle<T extends PacketType> = (packet: Packet<T>) => void
type CBHandleAll = (packet: _PacketVariant) => void

export var Peeker: typeof import("client");
export { CallProcedure } from "$lib/rpcbuilder";
export { GameMaster, type AcceptableValue } from "$lib/gamemaster";
export { StateManager } from "$lib/state";
export { Push } from "$lib/push"
export { Value } from "$lib/value";
export { PlayerManager } from "$lib/player"

async function ensure(socket: WebSocket, timeout = 10000) {
    const isOpened = () => (socket.readyState === WebSocket.OPEN)

    if (socket.readyState !== WebSocket.CONNECTING) {
        return isOpened()
    }
    else {
        const intrasleep = 250
        const ttl = timeout / intrasleep // time to loop
        let loop = 0
        while (socket.readyState === WebSocket.CONNECTING && loop < ttl) {
            await new Promise(resolve => setTimeout(resolve, intrasleep))
            loop++
        }
        return isOpened()
    }
}

export class Connection {
    ws!: WebSocket
    callbacks!: Map<PacketType, CBHandle<PacketType>[]>
    globalCB!: CBHandleAll[]
    public currentPart!: string

    static async create(): Promise<Connection> {
        Peeker = await import("client")
        let obj = new Connection();
        Peeker.ClientHandle.set_panic_hook()
        obj.ws = new WebSocket(`ws://${import.meta.env.VITE_WSENDPOINT}/harlem`);
        obj.callbacks = new Map()
        obj.globalCB = []
        obj.ws.onmessage = ((me) => {
            let packet: Packet<PacketType> = Peeker.ClientHandle.parse(me.data)
            if (packet.variant == Peeker.PacketType.Part) {
                // @ts-ignore: can never happen
                obj.currentPart = packet.value.name;
            }
            if (obj.callbacks.has(packet.variant)) {
                obj.callbacks.get(packet.variant)?.forEach((handle) => handle(packet));
            }
            // @ts-ignore
            obj.globalCB.forEach(async (handle) => handle(packet));
        })
        if (!await ensure(obj.ws)) {
            throw new Error("Unable to connect to host.")
        }

        return obj
    }

    on<T extends PacketType>(trigger: T, handle: CBHandle<T>): void
    on(trigger: "*", handle: CBHandleAll): void
    on(trigger: PacketType | "*", handle: CBHandleAll | CBHandle<PacketType>): void {
        if (trigger === "*") {
            this.globalCB.push(handle);
            return;
        }
        if (this.callbacks.has(trigger)) {
            // @ts-ignore
            this.callbacks.get(trigger)?.push(handle);
        } else {
            // @ts-ignore
            this.callbacks.set(trigger, [handle,])
        }
    }

    async send<T extends PacketType>(packet: Packet<T>) {
        this.ws.send(packet.pack());
    }
}
