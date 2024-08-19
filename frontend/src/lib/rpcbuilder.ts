import { preloadData } from "$app/navigation";
import { Peeker } from "$lib";
import type { Packet, PacketType, PortableType } from "client";

export class RPCBuilder {
    call!: Packet<PacketType.CallProcedure>

    constructor() {
        // @ts-ignore
        this.call = {
            variant: Peeker.PacketType.CallProcedure,
            value: {
                name: "",
                args: [],
            },
        }
    }

    name(name: string): RPCBuilder {
        this.call.value.name = name;
        return this;
    }

    arg(name: string, t: [] | number | string | boolean | null | object, type: "array" | "number" | "string" | "boolean" | "null" | "object") {
        let pv: PortableType;
        switch (type) {
            case "array":
                pv = Peeker.PortableType.ARRAY
            case "boolean":
                pv = Peeker.PortableType.BOOLEAN
            case "string":
                pv = Peeker.PortableType.STRING
            case "number":
                pv = Peeker.PortableType.NUMBER
            case "object":
                pv = Peeker.PortableType.OBJECT
            case "null":
                pv = Peeker.PortableType.NULL
        }


        this.call.value.args.push([name, {
            data: JSON.stringify(t),
            dataType: pv
        }])
    }

    build(): Packet<PacketType.CallProcedure> {
        return new Peeker.Packet(
            this.call.variant,
            this.call.value
        )
    }
}