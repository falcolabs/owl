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
    RequestResource = 9,
    ProcedureList = 10,
    CallProcedure = 11,
    GameState = 12,
    UpdateGameState = 13,
    Unknown = 14
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

export class Timer {
    startTime: Date;
    pausedTime: Date;
    pausedDuration: number;
    isPaused: boolean;

    pause(): never;
    resume(): never;
    elapsedSecs(): number;
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
    QuestionBank = 4,
    Show = 5,
    Ticker = 6,
    Timer = 7,
    CurrentPart = 8,
    AvailableProcedures = 9,
    GameState = 10
}

export class QueryPacket<T extends QueryType> {
    variant: T;
    value: QueryIndex<T>;

    constructor(variant: T, value: QueryIndex<T>);
}

export class Query {
    static player(value: string): Packet<PacketType.RequestResource>;
    static question(value: number): Packet<PacketType.RequestResource>;
    static partById(value: number): Packet<PacketType.RequestResource>;
    static partByName(value: string): Packet<PacketType.RequestResource>;
    static questionBank(): Packet<PacketType.RequestResource>;
    static show(): Packet<PacketType.RequestResource>;
    static ticker(): Packet<PacketType.RequestResource>;
    static timer(): Packet<PacketType.RequestResource>;
    static currentPart(): Packet<PacketType.RequestResource>;
    static availableProcedures(): Packet<PacketType.RequestResource>;
    static gameState(): Packet<PacketType.RequestResource>;
}

type QueryIndex<T> = T extends QueryType.Player
    ? string
    : T extends QueryType.Question
    ? number
    : T extends QueryType.PartByID
    ? number
    : T extends QueryType.PartByName
    ? string
    : null;

type QueryVariant =
    | { variant: QueryType.Player; index: string }
    | { variant: QueryType.Question; index: number }
    | { variant: QueryType.PartByID; index: number }
    | { variant: QueryType.PartByName; index: string }
    | { variant: QueryType.QuestionBank }
    | { variant: QueryType.Show }
    | { variant: QueryType.Ticker }
    | { variant: QueryType.Timer }
    | { variant: QueryType.CurrentPart }
    | { variant: QueryType.AvailableProcedures }
    | { variant: QueryType.GameState };

export type ProcedureSignature = {
    name: string;
    hidden: boolean;
    args: [string, PortableType][];
};

export type GameStatePrototype = {
    name: string;
    hidden: boolean;
    dataType: PortableType;
};

export type ProcedureCall = {
    name: string;
    args: [string, PortableValue][];
};

export type GameStateUpdate = {
    name: string;
    data: PortableValue;
};

export type AuthenticationStatus = {
    success: boolean;
    message: string;
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

export type PortableValue = {
    data: string;
    dataType: PortableType;
};

export class Packet<T extends PacketType> {
    variant: T;
    value: PacketValue<T>;

    constructor(packet: T, value: PacketValue<T>);
    pack(): string;
}

type PacketValue<T> = T extends PacketType.Player
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
    ? Timer
    : T extends PacketType.CommenceSession
    ? Credentials
    : T extends PacketType.AuthStatus
    ? AuthenticationStatus
    : T extends PacketType.RequestResource
    ? QueryVariant
    : T extends PacketType.ProcedureList
    ? ProcedureSignature[]
    : T extends PacketType.CallProcedure
    ? ProcedureCall
    : T extends PacketType.GameState
    ? GameStatePrototype[]
    : T extends PacketType.UpdateGameState
    ? GameStateUpdate
    : T extends PacketType.Unknown
    ? Unknown
    : never;

export type PacketVariant =
    | { variant: PacketType.Player; value: Player; pack: () => string; }
    | { variant: PacketType.Part; value: PartProperties; pack: () => string; }
    | { variant: PacketType.Question; value: Question; pack: () => string; }
    | { variant: PacketType.QuestionBank; value: QuestionBank; pack: () => string; }
    | { variant: PacketType.Show; value: Show; pack: () => string; }
    | { variant: PacketType.Ticker; value: Ticker; pack: () => string; }
    | { variant: PacketType.Timer; value: Timer; pack: () => string; }
    | { variant: PacketType.CommenceSession; value: Credentials; pack: () => string; }
    | { variant: PacketType.AuthStatus; value: AuthenticationStatus; pack: () => string; }
    | { variant: PacketType.RequestResource; value: QueryVariant; pack: () => string; }
    | { variant: PacketType.ProcedureList; value: ProcedureSignature[]; pack: () => string; }
    | { variant: PacketType.CallProcedure; value: ProcedureCall; pack: () => string; }
    | { variant: PacketType.GameState; value: GameStatePrototype[]; pack: () => string; }
    | { variant: PacketType.UpdateGameState; value: GameStateUpdate; pack: () => string; }
    | { variant: PacketType.Unknown; value: Unknown; pack: () => string; };

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