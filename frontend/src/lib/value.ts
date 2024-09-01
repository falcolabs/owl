import { Peeker } from "$lib";
import type { PortableType, PortableValue } from "client";

type AcceptableValue = any[] | number | string | boolean | null | object;

export class WASMValue {
    static create(value: AcceptableValue, type: PortableType): PortableValue {
        return new Peeker.PortableValue(
            JSON.stringify(value),
            type
        )
    }
    static array(t: any[]): PortableValue {
        return Value.create(t, Peeker.PortableType.ARRAY)
    }

    static number(t: number): PortableValue {
        return Value.create(t, Peeker.PortableType.NUMBER)
    }

    static string(t: string): PortableValue {
        return Value.create(t, Peeker.PortableType.STRING)
    }

    static null(): PortableValue {
        return Value.create(null, Peeker.PortableType.NULL)
    }

    static object(t: object): PortableValue {
        return Value.create(t, Peeker.PortableType.OBJECT)
    }
}

export class Value {
    static create(value: AcceptableValue, type: PortableType): PortableValue {
        return {
            data: JSON.stringify(value),
            dataType: type
        }
    }
    static array(t: any[]): PortableValue {
        return Value.create(t, Peeker.PortableType.ARRAY)
    }

    static number(t: number): PortableValue {
        return Value.create(t, Peeker.PortableType.NUMBER)
    }

    static string(t: string): PortableValue {
        return Value.create(t, Peeker.PortableType.STRING)
    }

    static null(): PortableValue {
        return Value.create(null, Peeker.PortableType.NULL)
    }

    static object(t: object): PortableValue {
        return Value.create(t, Peeker.PortableType.OBJECT)
    }
}
