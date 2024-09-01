// @ts-ignore
import { Packet, PacketType } from "../client";

export class Panel {
    free(): void;
    constructor();

    static inspect(t: any): void;
    static cpacket_test<T extends PacketType>(cp: Packet<T>): void;
}
