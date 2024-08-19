import engine
import utils
from config import config


class Auth(utils.PartImplementation):
    # def __init__(self):
    # self.props = engine.PartProperties("auth")

    def on_update(self, show: engine.Show) -> engine.Status:
        return engine.Status.RUNNING

    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        pass
