import engine
import pengin

class Auth(pengin.PartImplementation):
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
        print(f"got to auth yo {packet.data}")
