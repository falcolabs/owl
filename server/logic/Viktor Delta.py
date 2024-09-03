from typing import override
import engine
import penguin

class VD(penguin.PartImplementation):
    def __init__(self):
        super().__init__()

        self.rpc = penguin.RPCManager('TT')
        
        self.question_selections = self.rpc.use_state(
            "selected",
            [
                10,
                20,
                30
            ]
        )

        self.interject = self.rpc.use_state("interject","")

        self.rpc.add_procedures(
            [
                ("ring_bell", lambda _, callprod, _2, _3: self.interject.set(callprod.data.args[0][1].as_str()),[])
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
