from typing import override
import engine

import penguin
from config import config


class Standby(penguin.PartImplementation):
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
        pass
