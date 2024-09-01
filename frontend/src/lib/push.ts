import { Peeker, type AcceptableValue } from "$lib";
import type { Packet, PacketType, PortableType } from "client"

export class Push {
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
        return Push.create(name, t, Peeker.PortableType.ARRAY)
    }

    static number(name: string, t: number): Packet<PacketType.UpdateState> {
        return Push.create(name, t, Peeker.PortableType.NUMBER)
    }

    static string(name: string, t: string): Packet<PacketType.UpdateState> {
        return Push.create(name, t, Peeker.PortableType.STRING)
    }

    static null(name: string): Packet<PacketType.UpdateState> {
        return Push.create(name, null, Peeker.PortableType.NULL)
    }

    static object(name: string, t: object): Packet<PacketType.UpdateState> {
        return Push.create(name, t, Peeker.PortableType.OBJECT)
    }
}
