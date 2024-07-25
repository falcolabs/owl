import engine
import pengin
from config import config


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
        engine.log_debug("Packet received on message handler.")
        if not isinstance(packet, engine.Packet.Register):
            return
        for detail in config().credentials:
            if (detail.username, detail.accessKey) != (
                packet.data.username,
                packet.data.access_key,
            ):
                await handle.send(
                    engine.Packet.AuthStatus(
                        engine.AuthenticationStatus(
                            False, "Authentication failed: invalid credentials."
                        )
                    ).pack()
                )
                return
        await handle.send(
            engine.Packet.AuthStatus(
                engine.AuthenticationStatus(True, "Authenticated.")
            ).pack()
        )
