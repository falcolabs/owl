from typing import override
import engine
import penguin

class TT(penguin.PartImplementation):
    def __init__(self):
        super().__init__()

        self.rpc = penguin.RPCManager('TT')
        self.questions = self.rpc.use_state(
            [
                {"status":None,"content":"the early bird gets the worms","number":1},
                {"status":None,"content":"get the ducks in a row","number":2},
                {"status":None,"content":"cooking exercise","number":3},
                {"status":None,"content":"peak content","number":4}
            ]
        )

        self.images = self.rpc.use_state(
            [
                {"type":"image","path":"","part":1},
                {"type":"video","path":"","part":4}
            ]
        )

        self.prompt = self.rpc.use_state("prompt","why are you still here?")

        self.answers = self.rpc.use_state(
            [
                {"answer":"i am too dumb for this","time":0.5},
                {"answer":"why am i still here?","time":0.55},
                {"answer":"just to suffer","time":0.55},
                {"answer":"10 hours of Shuzo Matsuoka telling you not to give up","time":10}
            ]
        )

        @override
        async def on_request(
            self,
            show: engine.Show,
            packet: engine.Packet,
            handle: engine.IOHandle,
            addr: str
        ):
            (await self.rpc.handle(show, packet, handle, addr)).unwrap()
