import engine
import asyncio
import uvloop
import abc


class PartImplementation(abc.ABC):
    def on_update(self, show: engine.Show) -> engine.Status: ...
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ): ...


class Show(engine.Show):
    async def handle_webreq(self, req: engine.RawRequest):
        print(f"we've got something {req.handle} {req.sender} {req.content.data}")
        if not isinstance(req.content, engine.Packet.RequestResource):
            return
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
        self.loop.run_until_complete(self.handle_webreq(req))

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
        self.loop = uvloop.new_event_loop()
