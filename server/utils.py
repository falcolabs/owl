import engine
import uvloop
import abc
import inspect
import typing

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


LOOP = uvloop.new_event_loop()


class ShowBootstrap(engine.Show):
    async def handle_webreq(self, req: engine.RawRequest):
        print(f"we've got something {req.handle} {req.sender} {req.content.data}")
        if not isinstance(req.content, engine.Packet.RequestResource):
            if isinstance(req.content, engine.Packet.CommenceSession):
                for detail in config().credentials:
                    if (detail.username, detail.accessKey) != (
                        req.content.data.username,
                        req.content.data.access_key,
                    ):
                        await req.handle.send(
                            engine.Packet.AuthStatus(
                                engine.AuthenticationStatus(
                                    False, "Authentication failed: invalid credentials."
                                )
                            ).pack()
                        )
                        return
                await req.handle.send(
                    engine.Packet.AuthStatus(
                        engine.AuthenticationStatus(True, "Authenticated.")
                    ).pack()
                )
        res_req = req.content.data
        response: engine.Packet | None = None
        match res_req:
            case engine.ResourceRequest.Player():
                for p in self.players:
                    if p.identifier == res_req.index:
                        response = engine.Packet.Player(p)
            case engine.ResourceRequest.Question():
                response = engine.Packet.Question(
                    self.qbank.get_question(res_req.index)
                )
            case engine.ResourceRequest.QuestionBank():
                response = engine.Packet.QuestionBank(self.qbank)
            case engine.ResourceRequest.Show():
                response = engine.Packet.Show(self)
            case engine.ResourceRequest.Ticker():
                response = engine.Packet.Ticker(self.ticker)
            case engine.ResourceRequest.Timer():
                response = engine.Packet.Timer(self.timer)
            case engine.ResourceRequest.CurrentPart():
                response = engine.Packet.Part(self.parts[self.current_part].props)
            case _:
                await self.parts[self.current_part].implementation.on_request(
                    self, req.content, req.handle, req.sender
                )
        print(response)
        if response is not None:
            str_content = response.pack()
            print(f"Trying to send {str_content}")
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


def _to_portable_value(inp: str) -> engine.PortableValueName:
    if inp.startswith("list"):
        return "array"
    if inp.startswith("None"):
        return "null"
    if inp.startswith("int") or inp.startswith("float"):
        return "number"
    if inp.startswith("str"):
        return "string"
    if inp.startswith("dict") or inp.startswith("map"):
        return "object"
    else:
        raise TypeError(f"Unsupported argument type: `{inp}`")


ProcedureHandler = typing.Callable[
    [engine.Show, engine.Packet.CallProcedure, engine.IOHandle, str],
    None,
]

T = typing.TypeVar("T")


class WalkieTalkie:
    """Listens to & manages Remote Procedure Calls and updating GameState"""

    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.procedures: list[engine.Procedure] = []
        self.proc_map: dict[
            str,
            ProcedureHandler,
        ] = {}
        self.states: list[engine.GameStateValue] = []
        self.state_map: dict[str, object] = {}

    def synced_state(
        self, name: str, initial_value: T
    ) -> tuple[typing.Callable[[], T], typing.Callable[[T], None]]:

        self.state_map[name] = initial_value

        def get() -> T:
            return self.state_map[name]  # type: ignore

        def set(value: T):
            self.state_map[name] = value

        return get, set

    def add_procedure(
        self, proc: ProcedureHandler, hidden: bool = False, name: str | None = None
    ) -> "WalkieTalkie":
        n = name if name else proc.__name__
        self.procedures.append(
            engine.Procedure(
                name=self.prefix + "/" + n,
                hidden=hidden,
                args=[
                    (k, _to_portable_value(v.annotation))
                    for k, v in inspect.signature(proc).parameters.items()
                ],
            )
        )
        self.proc_map[n] = proc

        return self

    def add_procedures(
        self,
        proc_list: list[
            tuple[ProcedureHandler, bool]
            | tuple[str, ProcedureHandler, bool]
            | tuple[str, ProcedureHandler]
            | ProcedureHandler
        ],
    ) -> "WalkieTalkie":
        for maybe_tuple in proc_list:
            if isinstance(maybe_tuple, typing.Iterable):
                if isinstance(maybe_tuple[0], str):
                    if len(maybe_tuple) == 2 and isinstance(
                        maybe_tuple[1], typing.Callable
                    ):
                        self.add_procedure(maybe_tuple[1], name=maybe_tuple[0])
                    elif (
                        len(maybe_tuple) == 3
                        and isinstance(maybe_tuple[1], typing.Callable)
                        and isinstance(maybe_tuple[2], bool)
                    ):
                        self.add_procedure(
                            maybe_tuple[1], hidden=maybe_tuple[2], name=maybe_tuple[0]
                        )
                    else:
                        raise ValueError(f"Invalid procedure notation: `{maybe_tuple}`")
                elif len(maybe_tuple) == 2 and isinstance(maybe_tuple[1], bool):
                    self.add_procedure(maybe_tuple[0], hidden=maybe_tuple[1])
                else:
                    raise ValueError(f"Invalid procedure notation: `{maybe_tuple}`")
            else:
                self.add_procedure(maybe_tuple, False)

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
                    if proc.name() == call.name():
                        return self.proc_map[proc.name()](show, packet, handle, addr)
                else:
                    engine.log_error(
                        f"Cannot find procedure with name `{proc.name()}`. Call ignored."
                    )
            case engine.Packet.ProcedureList():
                await handle.send(engine.Packet.ProcedureList(self.procedures).pack())
