import engine
import abc
import platform
import os

from .session import SessionManager

from config import config

SESSION_MAN = SessionManager()
TASK_POOL: list = []
SHOW: "ShowBootstrap" = None  # type: ignore


class PartImplementation(abc.ABC):
    def on_update(self, show: engine.Show) -> engine.Status: ...
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ): ...


if platform.python_implementation() == "CPython" and platform.platform().startswith(
    "Linux"
):
    try:
        import uvloop  # type: ignore

        LOOP = uvloop.new_event_loop()
    except ImportError:
        engine.log_warning(
            "uvloop is not installed. If you are on Linux, uvloop drastically improve Python async performance. Falling back to asyncio."
        )
        import asyncio  # type: ignore

        LOOP = asyncio.new_event_loop()
else:
    engine.log_info(
        "Non-CPython implementation or non-Linux OS detected. Falling back to asyncio."
    )
    import asyncio  # type: ignore

    LOOP = asyncio.new_event_loop()


class ShowBootstrap(engine.Show):
    async def handle_webreq(self, req: engine.RawRequest):
        global TASK_POOL
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
                                False, "Authentication failed: invalid credentials.", ""
                            )
                        )
                        return
                token = SESSION_MAN.link_player(detail.username, req.handle)
                response = engine.Packet.AuthStatus(
                    engine.AuthenticationStatus(True, "Authenticated.", token)
                )
            if isinstance(req.content, engine.Packet.Unknown):
                if req.content.data == "CONNECTION INITIATED":
                    SESSION_MAN.register_session(req.handle)
                if req.content.data == "CONNECTION HALTED":
                    SESSION_MAN.purge(req.handle)
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
            case engine.Query.PlayerList():
                response = engine.Packet.PlayerList(self.players)
            case _:
                await self.parts[self.current_part].implementation.on_request(
                    self, req.content, req.handle, req.sender
                )
        if response is not None:
            str_content = response.pack()
            engine.log_debug(f"<- TO {req.sender}: {str_content}&r")
            await req.handle.send(str_content)

        # Process task pool entries
        for t in TASK_POOL:
            await t
        TASK_POOL = []

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
