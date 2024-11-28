from typing import final, override
import engine
import json
import penguin
from config import config
from penguin.rpc import RPCManager


@final
class TKD(penguin.PartImplementation):
    def __init__(self):
        super().__init__()
        self.rpc = RPCManager("tkd")
        self.org_list: dict[str, dict] = {}
        self.appear = self.rpc.use_state("appear", {})

        self.rpc.add_procedures([("show_next", self.show_next, [])])

    def show_next(
        self,
        show: penguin.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        addr: str,
    ):
        ktr = list(self.org_list.keys())[0]
        val = self.org_list.pop(ktr)
        a = self.appear.get()
        a[ktr] = val
        self.appear.set(a)

    @override
    def on_ready(self, show: penguin.Show):
        p = []
        for i in self.show.players.get():
            p.append(json.loads(i.pack()))
        p.sort(key=lambda x: x["score"], reverse=True)

        for pl in p:
            self.org_list[pl["identifier"]] = {
                "displayName": pl["name"],
                "score": pl["score"],
            }

    @override
    def on_update(self, show: penguin.Show) -> engine.Status:
        return engine.Status.RUNNING

    @override
    async def on_request(
        self,
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
