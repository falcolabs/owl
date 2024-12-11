// TODO - reenable automatic generation so
// changing Rust code does not lead to changing TS types.
export enum PacketType {
    Player,
    Part,
    Question,
    QuestionBank,
    Ticker,
    Timer,
    CommenceSession,
    AuthStatus,
    Query,
    ProcedureList,
    CallProcedure,
    StateList,
    State,
    UpdateState,
    Unknown,
    PlayerList,
    PartList,
    PlaySound,
    NextAnimation,
    LogEntry,
}

export type Player = {
    identifier: string;
    name: string;
    score: number;
};
export type PartProperties = {
    name: string;
};

export type MediaContent = {
    mediaType: "video" | "image" | "audio",
    uri: string
}

export type Question = {
    prompt: string;
    media: MediaContent;
    key: string;
    score: number;
    time: number;
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

export type LogEntry = {
    timestamp: number,
    level: number,
    logger: string,
    content: string,
}

export class Timer {
    startTime: ServerTime;
    pausedTime: ServerTime;
    pausedDuration: ServerDuration;

    constructor();
    static from(obj: TimerLike): Timer
    isPaused(): boolean;
    pause(): void;
    resume(): void;
    elapsedSecs(): number;
    pack(): string;
}

export type Ticker = {
    lastTick: string;
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
    Ticker = 7,
    Timer = 8,
    CurrentPart = 9,
    AvailableProcedures = 10,
    StateList = 11,
    PartList = 12,
    Log = 13,
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
    static ticker(): Packet<PacketType.Query>;
    static timer(): Packet<PacketType.Query>;
    static currentPart(): Packet<PacketType.Query>;
    static availableProcedures(): Packet<PacketType.Query>;
    static stateList(): Packet<PacketType.Query>;
    static partList(): Packet<PacketType.Query>;
    static log(value: number): Packet<PacketType.Query>;
}

type _QueryIndex<T> = T extends QueryType.Player
    ? string
    : T extends QueryType.Question
    ? number
    : T extends QueryType.PartByID
    ? number
    : T extends QueryType.PartByName
    ? string
    : T extends QueryType.Log
    ? number
    : QueryType;

type _QueryVariant =
    | { variant: QueryType.Player; index: string }
    | { variant: QueryType.Question; index: number }
    | { variant: QueryType.PartByID; index: number }
    | { variant: QueryType.PartByName; index: string }
    | { variant: QueryType.QuestionBank }
    | { variant: QueryType.State }
    | { variant: QueryType.StateList }
    | { variant: QueryType.PartList }
    | { variant: QueryType.PlayerList }
    | { variant: QueryType.Ticker }
    | { variant: QueryType.Timer }
    | { variant: QueryType.CurrentPart }
    | { variant: QueryType.AvailableProcedures }
    | { variant: QueryType.Log };

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
    : T extends PacketType.PartList
    ? PartProperties[]
    : T extends PacketType.PlaySound
    ? string
    : T extends PacketType.NextAnimation
    ? string
    : T extends PacketType.LogEntry
    ? LogEntry
    : never;

export type _PacketVariant =
    | { variant: PacketType.Player; value: Player; pack: () => string; }
    | { variant: PacketType.Part; value: PartProperties; pack: () => string; }
    | { variant: PacketType.Question; value: Question; pack: () => string; }
    | { variant: PacketType.QuestionBank; value: QuestionBank; pack: () => string; }
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
    | { variant: PacketType.PlayerList; value: Player[]; pack: () => string; }
    | { variant: PacketType.PlayerList; value: Player[]; pack: () => string; }
    | { variant: PacketType.PlaySound; value: string; pack: () => string; }
    | { variant: PacketType.NextAnimation; value: string; pack: () => string; }
    | { variant: PacketType.LogEntry; value: LogEntry; pack: () => string; };

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

export type AvailableSound = "op-introduction"
    | "op-introducecontestants"
    | "op-introduceguest"
    | "common-startsection"
    | "common-dotdotdot"
    | "common-scoresum"
    | "tongket-4th"
    | "tongket-3rd"
    | "tongket-2nd"
    | "tongket-1st"
    | "tongket-award"
    | "khoidong-start"
    | "khoidong-ready"
    | "khoidong-3secs"
    | "khoidong-bgm"
    | "khoidong-correct"
    | "khoidong-incorrect"
    | "khoidong-bell"
    | "khoidong-complete"
    | "vcnv-start"
    | "vcnv-questionbox"
    | "vcnv-selectrow"
    | "vcnv-showquestion"
    | "vcnv-15secs"
    | "vcnv-showanswers"
    | "vcnv-correct"
    | "vcnv-incorrect"
    | "vcnv-open"
    | "vcnv-bell"
    | "vcnv-bellcorrect"
    | "tangtoc-start"
    | "tangtoc-revealquestion"
    | "tangtoc-10secs"
    | "tangtoc-20secs"
    | "tangtoc-30secs"
    | "tangtoc-40secs"
    | "tangtoc-showanswers"
    | "tangtoc-correct"
    | "tangtoc-wrong"
    | "vedich-start"
    | "vedich-onstage"
    | "vedich-packagechoice"
    | "vedich-confirmchoice"
    | "vedich-15secs"
    | "vedich-20secs"
    | "vedich-star"
    | "vedich-poll"
    | "vedich-bell"
    | "vedich-correct"
    | "vedich-complete"
