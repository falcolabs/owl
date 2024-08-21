import { Peeker } from "$lib";
import type { Packet, PacketType, PortableType, PortableValue } from "client";
import { Value } from "./value";

export class CallProcedure {
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

    static name(name: string): CallProcedure {
        let obj = new CallProcedure();
        obj.call.value.name = name;
        return obj;
    }

    arg(name: string, pv: PortableValue): CallProcedure {
        this.call.value.args.push([name, pv])
        return this;
    }

    array(name: string, arr: any[]): CallProcedure {
        return this.arg(name, Value.array(arr))
    }

    number(name: string, num: number): CallProcedure {
        return this.arg(name, Value.number(num))
    }

    string(name: string, str: string): CallProcedure {
        return this.arg(name, Value.string(str))
    }

    null(name: string): CallProcedure {
        return this.arg(name, Value.null())
    }

    object(name: string, obj: object): CallProcedure {
        return this.arg(name, Value.object(obj))
    }

    build(): Packet<PacketType.CallProcedure> {
        console.log(this.call.value)
        return new Peeker.Packet(
            this.call.variant,
            this.call.value
        )
    }
}