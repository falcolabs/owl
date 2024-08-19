// place files you want to import through the `$lib` alias in this folder.

export const ORG_NAME: string = "CBN Shitposter Association · THPT Chuyên Bắc Ninh";
export const SHOW_NAME: string = "Đáy xã hội 2";

import type { PacketType, Packet, PacketVariant } from "client";
type CBHandle = (packet: PacketVariant) => void

export var Peeker: typeof import("client");
export { RPCBuilder } from "$lib/rpcbuilder";

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
    callbacks!: Map<PacketType, CBHandle[]>
    global_cb!: CBHandle[]

    static async create(): Promise<Connection> {
        Peeker = await import("client")
        let obj = new Connection();
        Peeker.ClientHandle.set_panic_hook()
        obj.ws = new WebSocket("ws://localhost:6942/harlem");
        obj.callbacks = new Map()
        obj.global_cb = []
        obj.ws.onmessage = ((me) => {
            let packet: Packet<PacketType> = Peeker.ClientHandle.parse(me.data)
            if (obj.callbacks.has(packet.variant)) {
                // @ts-ignore
                obj.callbacks.get(packet.variant)?.forEach((handle) => handle(packet));
            }
            // @ts-ignore
            obj.global_cb.forEach((handle) => handle(packet));
        })
        if (!await ensure(obj.ws)) {
            throw new Error("Unable to connect to host.")
        }

        return obj
    }

    on(trigger: PacketType | "*", handle: CBHandle) {
        if (trigger === "*") {
            this.global_cb.push(handle);
            return;
        }
        if (this.callbacks.has(trigger)) {
            this.callbacks.get(trigger)?.push(handle);
        } else {
            this.callbacks.set(trigger, [handle,])
        }
    }

    async send<T extends PacketType>(packet: Packet<T>) {
        this.ws.send(packet.pack());
    }
}