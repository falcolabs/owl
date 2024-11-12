from typing import final, override
import typing
import engine
import abc
import asyncio
import json
from .session import SessionManager
from .store import Writable
from utils.crypt import gen_token


from config import config

SESSION_MAN = SessionManager()
TASK_POOL: list = []


class PartImplementation:
    show: "Show"
    session_manager: SessionManager

    def on_ready(self, show: "Show"):
        pass

    def on_update(self, show: "Show") -> engine.Status:
        return engine.Status.RUNNING

    async def on_request(
        self,
        show: "Show",
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        pass


# if platform.python_implementation() == "CPython" and platform.platform().startswith(
#     "Linux"
# ):
#     try:
#         import uvloop

#         LOOP = uvloop.new_event_loop()
#     except ImportError:
#         engine.log_warning(
#             "uvloop is not installed. If you are on Linux, uvloop drastically improve Python async performance. Falling back to asyncio."
#         )
#         import asyncio

#         LOOP = asyncio.new_event_loop()
# else:
# engine.log_info(
#     "Non-CPython implementation or non-Linux OS detected. Falling back to asyncio."
# )
LOOP = asyncio.new_event_loop()


@final
class Show:
    async def handle_webreq(self, req: engine.RawRequest):
        engine.log_debug(
            engine.mccolor(f"&1> ") + f"{req.sender}: {req.content.pack()}"
        )
        self.session_manager.register_session(req.handle)

        # Process task pool entries
        global TASK_POOL
        for t in TASK_POOL:
            await t
        TASK_POOL = []
        (await self.rpc.handle(self, req.content, req.handle, req.sender)).unwrap()
        response: engine.Packet | None = None
        if not isinstance(req.content, engine.Packet.Query):
            if isinstance(req.content, engine.Packet.CommenceSession):
                for detail in config().credentials:
                    if (detail.username, detail.accessKey) == (
                        req.content.data.username,
                        req.content.data.access_key,
                    ):
                        token = self.session_manager.link_player(
                            detail.username, req.handle
                        )
                        print(self.session_manager.player_map)
                        response = engine.Packet.AuthStatus(
                            engine.AuthenticationStatus(True, "Authenticated.", token)
                        )
                        break
                else:
                    response = engine.Packet.AuthStatus(
                        engine.AuthenticationStatus(
                            False, "Authentication failed: invalid credentials.", ""
                        )
                    )
            if isinstance(req.content, engine.Packet.Unknown):
                if req.content.data == "CONNECTION INITIATED":
                    self.session_manager.register_session(req.handle)
                if req.content.data == "CONNECTION HALTED":
                    self.session_manager.purge(req.handle)
        res_req = req.content.data
        match res_req:
            case engine.Query.Player():
                for p in self.players.get():
                    if p.identifier == res_req.index:
                        response = engine.Packet.Player(p)
                else:
                    engine.log_warning(
                        f"Player '{res_req.index}' not found. All registered players are {[i.identifier for i in self.players.get()]}. Ignoring request."
                    )
            case engine.Query.Question():
                response = engine.Packet.Question(
                    self.qbank.get_question(res_req.index)
                )
            case engine.Query.QuestionBank():
                response = engine.Packet.QuestionBank(self.qbank)
            case engine.Query.Ticker():
                response = engine.Packet.Ticker(self.ticker)
            case engine.Query.Timer():
                response = engine.Packet.Timer(self.timer.get())
            case engine.Query.CurrentPart():
                response = engine.Packet.Part(self.parts[self.current_part.get()].props)
            case engine.Query.PlayerList():
                response = engine.Packet.PlayerList(self.players.get())
            case engine.Query.PartList():
                response = engine.Packet.PartList([p.props for p in self.parts])
            case _:
                await self.parts[self.current_part.get()].implementation.on_request(
                    self, req.content, req.handle, req.sender
                )
        if response is not None:
            str_content = response.pack()
            engine.log_debug(engine.mccolor(f"&6< ") + f"{req.sender}: {str_content}")
            await req.handle.send(str_content)

    def on_req(self, req: engine.RawRequest):
        LOOP.run_until_complete(self.handle_webreq(req))

    def start(self, listen_on: str, serve_on: str, static_dir: str):
        engine.log_info("Starting show...")
        engine.ws_task(
            listen_on,
            serve_on,
            static_dir,
            self.on_req,
        )

        for p in self.parts:
            p.implementation.show = self  # type: ignore[reportAttributeAccessIssue]
            p.implementation.session_manager = SESSION_MAN  # type: ignore[reportAttributeAccessIssue]
            p.implementation.on_ready(self)  # type: ignore[reportAttributeAccessIssue]

        self.ticker: engine.Ticker = engine.Ticker()
        part = self.parts[self.current_part.get()]
        while True:
            # TODO - remove this if there are no parts that require a loop
            status = part.implementation.on_update(self)
            match status:
                case engine.Status.STOP:
                    engine.log_info("Show stopped by logic.")
                    exit(0)
                case engine.Status.SKIP:
                    if self.current_part.get() >= len(self.parts):
                        engine.log_info(
                            "There is no more parts after this in the show."
                        )
                        exit(0)
                    self.current_part.set(self.current_part.get() + 1)
                    part = self.parts[self.current_part.get()]
                case engine.Status.REWIND:
                    if self.current_part.get() == len(self.parts):
                        engine.log_info(
                            "There is no more parts in front of this in the show."
                        )
                        exit(0)
                    self.current_part.set(self.current_part.get() - 1)
                    part = self.parts[self.current_part.get()]
                case _:
                    pass

        # return super().start(listen_on, serve_on, static_dir)

    def set_part(
        self,
        _: "Show",
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        addr: str,
    ):
        new_part = call.data.int_argno(0)
        self.current_part.set(new_part)

    def timer_operation(
        self,
        _: "Show",
        callproc: engine.Packet.CallProcedure,
        _2: engine.IOHandle,
        _3,
    ):
        operation: typing.Literal["start", "pause", "reset"] | str = json.loads(
            callproc.data.argno(0).json
        )
        engine.log_debug(f"Processing timer operation: {operation}")
        t = self.timer.get()
        match operation:
            case "start":
                t.resume()
            case "pause":
                t.pause()
                engine.log_debug(f"paused time: {t.time_elapsed()}")
            case "reset":
                t = engine.Timer()
            case _:
                engine.log_warning(f"Timer operation not found: {operation}. Ignoring.")

        self.timer.set(t)

    def __init__(
        self,
        name: str,
        parts: list[engine.Part],
        players: list[engine.Player],
        tick_speed: int,
        question_bank: engine.QuestionBank,
    ):
        from .rpc import RPCManager

        global SESSION_MAN
        self.rpc: RPCManager = RPCManager("engine")

        self.name: str = name
        self.parts: list[engine.Part] = parts
        self.available_parts: Writable[dict] = self.rpc.use_state(
            "available_parts", {i: v.props.name for i, v in enumerate(parts)}
        )

        def _ser_players(inp: list[engine.Player]) -> engine.PortableValue:
            return engine.PortableValue(
                json.dumps([i.pack() for i in inp]), engine.PortableType.OBJECT
            )

        def _der_players(inp: engine.PortableValue) -> list[engine.Player]:
            return [
                engine.Player.from_json(json.dumps(i)) for i in json.loads(inp.json)
            ]

        self.players: Writable[list[engine.Player]] = self.rpc.use_state(
            "engine_players",
            players,
            serializer=_ser_players,
            deserializer=_der_players,
        )
        self.tick_speed: int = tick_speed
        self.qbank: engine.QuestionBank = question_bank
        self.current_part: Writable[int] = self.rpc.use_state("current_part", 0)
        self.ticker = engine.Ticker()
        self.sid: Writable[str] = self.rpc.use_state("sid", gen_token(8))
        self.session_manager = SESSION_MAN
        self.timer: Writable[engine.Timer] = self.rpc.use_state(
            "timer",
            engine.Timer(),
            serializer=lambda x: engine.PortableValue(
                x.pack(), engine.PortableType.OBJECT
            ),
            deserializer=lambda x: engine.Timer.from_json(x.json),
        )

        self.rpc.add_procedures(
            [
                ("set_part", self.set_part, [("index", engine.PortableType.NUMBER)]),
                (
                    "timer_operation",
                    self.timer_operation,
                    [("operation", engine.PortableType.STRING)],
                ),
            ]
        )