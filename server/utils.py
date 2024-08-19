import engine
import abc
import inspect
import typing
import json
import platform

from config import config


class PartImplementation(abc.ABC):
    def on_update(self, show: engine.Show) -> engine.Status: ...
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ): ...


if platform.python_implementation() == "CPython":
    import uvloop  # type: ignore

    LOOP = uvloop.new_event_loop()
else:
    import asyncio  # type: ignore

    LOOP = asyncio.new_event_loop()


class ShowBootstrap(engine.Show):
    async def handle_webreq(self, req: engine.RawRequest):
        response: engine.Packet | None = None
        engine.log_debug(
            engine.mccolor(f"-> FROM {req.sender}: {req.content.pack()}&r")
        )
        if not isinstance(req.content, engine.Packet.Query):
            if isinstance(req.content, engine.Packet.CommenceSession):
                for detail in config().credentials:
                    if (detail.username, detail.accessKey) != (
                        req.content.data.username,
                        req.content.data.access_key,
                    ):
                        response = engine.Packet.AuthStatus(
                            engine.AuthenticationStatus(
                                False, "Authentication failed: invalid credentials."
                            )
                        )
                        return
                response = engine.Packet.AuthStatus(
                    engine.AuthenticationStatus(True, "Authenticated.")
                )
        res_req = req.content.data
        match res_req:
            case engine.Query.Player():
                for p in self.players:
                    if p.identifier == res_req.index:
                        response = engine.Packet.Player(p)
                else:
                    engine.log_warning(
                        f"Player '{res_req.index}' not found. All registered players are {[i.identifier for i in self.players]}. Ignoring request."
                    )
            case engine.Query.Question():
                response = engine.Packet.Question(
                    self.qbank.get_question(res_req.index)
                )
            case engine.Query.QuestionBank():
                response = engine.Packet.QuestionBank(self.qbank)
            case engine.Query.Show():
                response = engine.Packet.Show(self)
            case engine.Query.Ticker():
                response = engine.Packet.Ticker(self.ticker)
            case engine.Query.Timer():
                response = engine.Packet.Timer(self.timer)
            case engine.Query.CurrentPart():
                response = engine.Packet.Part(self.parts[self.current_part].props)
            case _:
                await self.parts[self.current_part].implementation.on_request(
                    self, req.content, req.handle, req.sender
                )
        if response is not None:
            str_content = response.pack()
            engine.log_info(engine.mccolor(f"&a<- TO {req.sender}: {str_content}&r"))
            await req.handle.send(str_content)

    def on_req(self, req: engine.RawRequest):
        LOOP.run_until_complete(self.handle_webreq(req))

    def start(self, listen_on: str, serve_on: str, static_dir: str):
        engine.log_info("Starting show...")
        engine.Show.ws_task(
            listen_on,
            serve_on,
            static_dir,
            self.on_req,
        )
        self.ticker = engine.Ticker()
        part = self.parts[self.current_part]
        while True:
            status = part.implementation.on_update(self)
            match status:
                case engine.Status.STOP:
                    engine.log_info("Show stopped by logic.")
                    exit(0)
                case engine.Status.SKIP:
                    if self.current_part >= len(self.parts):
                        engine.log_info(
                            "There is no more parts after this in the show."
                        )
                        exit(0)
                    self.current_part += 1
                    part = self.parts[self.current_part]
                case engine.Status.REWIND:
                    if self.current_part == len(self.parts):
                        engine.log_info(
                            "There is no more parts in front of this in the show."
                        )
                        exit(0)
                    self.current_part -= 1
                    part = self.parts[self.current_part]

        # return super().start(listen_on, serve_on, static_dir)

    def __init__(
        self,
        name: str,
        parts: list[engine.Part],
        players: list[engine.Player],
        tick_speed: int,
        question_bank: engine.QuestionBank,
    ):
        self.name = name
        self.parts = parts
        self.players = players
        self.tick_speed = tick_speed
        self.qbank = question_bank
        self.current_part = 0
        self.ticker = engine.Ticker()
        self.timer = engine.Timer()


def str_portable_type(inp: str) -> engine.PortableType:
    if inp.startswith("list"):
        return engine.PortableType.ARRAY
    if inp.startswith("None"):
        return engine.PortableType.NULL
    if inp.startswith("int") or inp.startswith("float"):
        return engine.PortableType.NUMBER
    if inp.startswith("str"):
        return engine.PortableType.STRING
    if inp.startswith("dict") or inp.startswith("map"):
        return engine.PortableType.OBJECT
    else:
        raise TypeError(f"Unsupported argument type: `{inp}`")


def portable_type(inp: object) -> engine.PortableType:
    if isinstance(inp, list):
        return engine.PortableType.ARRAY
    if inp is None:
        return engine.PortableType.NULL
    if isinstance(inp, int) or isinstance(inp, float):
        return engine.PortableType.NUMBER
    if isinstance(inp, str):
        return engine.PortableType.STRING
    if isinstance(inp, dict) or isinstance(inp, map):
        return engine.PortableType.OBJECT
    else:
        raise TypeError(f"Unsupported argument type: `{inp}`")


ProcedureHandler = typing.Callable[
    [engine.Show, engine.Packet.CallProcedure, engine.IOHandle, str],
    None,
]

T = typing.TypeVar("T", list, int, float, str, dict)
Signature = list[tuple[str, engine.PortableType]]


class Is:
    """Basic typechecking class"""

    @staticmethod
    def proc(v: typing.Any):
        return isinstance(v, typing.Callable)

    @staticmethod
    def str(v: typing.Any):
        return isinstance(v, str)

    @staticmethod
    def signature(v: typing.Any):
        return isinstance(v, typing.Iterable) and not isinstance(v, str)

    @staticmethod
    def bool(v: typing.Any):
        return isinstance(v, bool)


class WalkieTalkie:
    """Listens to & manages Remote Procedure Calls and updating GameState"""

    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.procedures: list[engine.ProcedureSignature] = []
        self.proc_map: dict[
            str,
            ProcedureHandler,
        ] = {}
        self.states: list[engine.GameStatePrototype] = []
        self.state_map: dict[str, object] = {}

    def use_state(
        self, name: str, initial_value: T, hidden=False
    ) -> tuple[typing.Callable[[], T], typing.Callable[[T], None]]:
        ptype = portable_type(initial_value)
        self.states.append(
            engine.GameStatePrototype(name=name, hidden=hidden, data_type=ptype)
        )
        self.state_map[name] = initial_value

        def get() -> T:
            return self.state_map[name]  # type: ignore

        def set(value: T):
            if config().checkRPCTypes and ptype != portable_type(value):
                raise TypeError(
                    f"Type mismatch: expected '{ptype}', found '{portable_type(value)}'"
                )
            # for i, v in enumerate(self.states):
            #     if v.name() == name:
            #         self.states[i] = engine.GameStatePrototype(name=name, hidden=hidden, data_type=portable_type(value))
            self.state_map[name] = value

        return get, set

    def add_procedure(
        self,
        proc: ProcedureHandler,
        *,
        signature: Signature,
        hidden: bool = False,
        name: str | None = None,
    ) -> "WalkieTalkie":
        n = name if name else proc.__name__
        proc_ident = self.prefix + "::" + n
        self.procedures.append(
            engine.ProcedureSignature(
                name=proc_ident,
                hidden=hidden,
                args=signature,
            )
        )
        self.proc_map[proc_ident] = proc

        return self

    def add_procedures(
        self,
        proc_list: list[
            tuple[ProcedureHandler, bool, Signature]
            | tuple[str, ProcedureHandler, bool, Signature]
            | tuple[str, ProcedureHandler, Signature]
            | tuple[ProcedureHandler, Signature]
        ],
    ) -> "WalkieTalkie":
        for t in proc_list:
            match t:
                case (p1, p2, p3, signature):
                    self.add_procedure(p2, name=p1, hidden=p3, signature=signature)
                case (p1, p2, signature):
                    if Is.proc(p1) and Is.bool(p2):
                        self.add_procedure(p1, hidden=p2, signature=signature)  # type: ignore
                    if Is.str(p1) and Is.proc(p2):
                        self.add_procedure(p2, name=p1, signature=signature)  # type: ignore
                case (p1, signature):
                    self.add_procedure(p1, signature=signature)
                case _:
                    raise ValueError(f"Unknown procedure prototype: {t}")

        return self

    async def handle(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        match packet:
            case engine.Packet.CallProcedure():
                call = packet.data
                for proc in self.procedures:
                    if proc.name == call.name:
                        engine.log_debug(f"Calling procedure {call.name}")
                        # TODO - type checking for procedure arguments.
                        return self.proc_map[proc.name](show, packet, handle, addr)
                else:
                    engine.log_error(
                        f"Cannot find procedure with name `{proc.name}`. Call ignored."
                    )
            case engine.Packet.Query():
                request = packet.data
                match request:
                    case engine.Query.AvailableProcedures():
                        await handle.send(
                            engine.Packet.ProcedureList(self.procedures).pack()
                        )
                    case engine.Query.GameState():
                        await handle.send(engine.Packet.GameState(self.states).pack())
            case engine.Packet.UpdateGameState():
                update = packet.data
                for state in self.states:
                    if state.name == update.name:
                        self.state_map[state.name] = json.loads(update.data.json)
