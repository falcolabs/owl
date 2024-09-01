// TODO - reenable automatic generation so
// changing Rust code does not lead to changing TS types.
export enum PacketType {
    Player = 0,
    Part = 1,
    Question = 2,
    QuestionBank = 3,
    Show = 4,
    Ticker = 5,
    Timer = 6,
    CommenceSession = 7,
    AuthStatus = 8,
    Query = 9,
    ProcedureList = 10,
    CallProcedure = 11,
    StateList = 12,
    State = 13,
    UpdateState = 14,
    Unknown = 15,
    PlayerList = 16,
}

export type Player = {
    identifier: string;
    name: string;
    score: number;
};
export type PartProperties = {
    name: string;
};
export type Question = {
    prompt: string;
    key: string;
    score: number;
    choices: string[];
    scoreFalse: number;
    explaination: string;
};
export type QuestionBank = {
    questionBank: Question[];
};

type ServerTime = {
    secs_since_epoch: number,
    nanos_since_epoch: number
};

type ServerDuration = {
    secs: number,
    nanos: number
};

export type TimerLike = {
    startTime: ServerTime;
    pausedTime: ServerTime;
    pausedDuration: ServerDuration;
    isPaused: boolean;
}

export class Timer {
    startTime: ServerTime;
    pausedTime: ServerTime;
    pausedDuration: ServerDuration;
    isPaused: boolean;

    constructor();
    static from(obj: object): Timer
    pause(): void;
    resume(): void;
    elapsedSecs(): number;
    pack(): string;
}

export type Ticker = {
    lastTick: string;
};
export type Show = {
    /** The name of the show. */
    name: string;
    /** The show's tick speed. */
    tickSpeed: number;
    /** The current part index. */
    currentPart: number;
    /** The players present */
    players: Player[];
    /** All the questions the show contains */
    qbank: QuestionBank;
    /** The show's ticker */
    ticker: Ticker;
    /** The show's timer */
    timer: Timer;
};

export type Credentials = {
    username: string;
    accessKey: string;
};

export enum QueryType {
    Player = 0,
    Question = 1,
    PartByID = 2,
    PartByName = 3,
    State = 4,
    PlayerList = 5,
    QuestionBank = 6,
    Show = 7,
    Ticker = 8,
    Timer = 9,
    CurrentPart = 10,
    AvailableProcedures = 11,
    StateList = 12,
}

export class QueryPacket<T extends QueryType> {
    variant: T;
    value: _QueryIndex<T>;

    constructor(variant: T, value: _QueryIndex<T>);
}

export class Query {
    static player(value: string): Packet<PacketType.Query>;
    static question(value: number): Packet<PacketType.Query>;
    static partById(value: number): Packet<PacketType.Query>;
    static partByName(value: string): Packet<PacketType.Query>;
    static state(value: string): Packet<PacketType.Query>;
    static playerList(): Packet<PacketType.Query>;
    static questionBank(): Packet<PacketType.Query>;
    static show(): Packet<PacketType.Query>;
    static ticker(): Packet<PacketType.Query>;
    static timer(): Packet<PacketType.Query>;
    static currentPart(): Packet<PacketType.Query>;
    static availableProcedures(): Packet<PacketType.Query>;
    static stateList(): Packet<PacketType.Query>;
}

type _QueryIndex<T> = T extends QueryType.Player
    ? string
    : T extends QueryType.Question
    ? number
    : T extends QueryType.PartByID
    ? number
    : T extends QueryType.PartByName
    ? string
    : null;

type _QueryVariant =
    | { variant: QueryType.Player; index: string }
    | { variant: QueryType.Question; index: number }
    | { variant: QueryType.PartByID; index: number }
    | { variant: QueryType.PartByName; index: string }
    | { variant: QueryType.QuestionBank }
    | { variant: QueryType.State }
    | { variant: QueryType.PlayerList }
    | { variant: QueryType.Show }
    | { variant: QueryType.Ticker }
    | { variant: QueryType.Timer }
    | { variant: QueryType.CurrentPart }
    | { variant: QueryType.AvailableProcedures };

export type ProcedureSignature = {
    name: string;
    hidden: boolean;
    args: [string, PortableType][];
};

export type ProcedureCall = {
    name: string;
    args: [string, PortableValue][];
};

export type GameState = {
    name: string;
    data: PortableValue;
};

export type AuthenticationStatus = {
    success: boolean;
    message: string;
    token: string;
};

export type Unknown = string;

export enum PortableType {
    ARRAY = 0,
    NUMBER = 1,
    STRING = 2,
    NULL = 3,
    OBJECT = 4,
    BOOLEAN = 5
}

export class PortableValue {
    data: string;
    dataType: PortableType;

    constructor(data: string, dataType: PortableType)
}

export class Packet<T extends PacketType> {
    variant: T;
    value: _PacketValue<T>;

    constructor(packet: T, value: _PacketValue<T>);
    pack(): string;
}

export type _PacketValue<T> = T extends PacketType.Player
    ? Player
    : T extends PacketType.Part
    ? PartProperties
    : T extends PacketType.Question
    ? Question
    : T extends PacketType.QuestionBank
    ? QuestionBank
    : T extends PacketType.Show
    ? Show
    : T extends PacketType.Ticker
    ? Ticker
    : T extends PacketType.Timer
    ? TimerLike
    : T extends PacketType.CommenceSession
    ? Credentials
    : T extends PacketType.AuthStatus
    ? AuthenticationStatus
    : T extends PacketType.Query
    ? _QueryVariant
    : T extends PacketType.ProcedureList
    ? ProcedureSignature[]
    : T extends PacketType.CallProcedure
    ? ProcedureCall
    : T extends PacketType.StateList
    ? GameState[]
    : T extends PacketType.State
    ? GameState
    : T extends PacketType.UpdateState
    ? GameState
    : T extends PacketType.Unknown
    ? Unknown
    : T extends PacketType.PlayerList
    ? Player[]
    : never;

export type _PacketVariant =
    | { variant: PacketType.Player; value: Player; pack: () => string; }
    | { variant: PacketType.Part; value: PartProperties; pack: () => string; }
    | { variant: PacketType.Question; value: Question; pack: () => string; }
    | { variant: PacketType.QuestionBank; value: QuestionBank; pack: () => string; }
    | { variant: PacketType.Show; value: Show; pack: () => string; }
    | { variant: PacketType.Ticker; value: Ticker; pack: () => string; }
    | { variant: PacketType.Timer; value: TimerLike; pack: () => string; }
    | { variant: PacketType.CommenceSession; value: Credentials; pack: () => string; }
    | { variant: PacketType.AuthStatus; value: AuthenticationStatus; pack: () => string; }
    | { variant: PacketType.Query; value: _QueryVariant; pack: () => string; }
    | { variant: PacketType.ProcedureList; value: ProcedureSignature[]; pack: () => string; }
    | { variant: PacketType.CallProcedure; value: ProcedureCall; pack: () => string; }
    | { variant: PacketType.StateList; value: GameState[]; pack: () => string; }
    | { variant: PacketType.State; value: GameState; pack: () => string; }
    | { variant: PacketType.UpdateState; value: GameState; pack: () => string; }
    | { variant: PacketType.Unknown; value: Unknown; pack: () => string; }
    | { variant: PacketType.PlayerList; value: Player[]; pack: () => string; };

/** Infrastructure for sending and handling {@link Packet}. */
export class ClientHandle {
    /** Frees the memory occupied by this object. */
    free(): void;
    static wrap(send_hook: (content: String) => any): ClientHandle
    static parse<T extends PacketType>(message: String): Packet<T>

    send<T extends PacketType>(packet: Packet<T>): Promise<null>;

    /**
     * Fishes out pesky panics and returns nice errors.
     */
    static set_panic_hook(): void;
}
