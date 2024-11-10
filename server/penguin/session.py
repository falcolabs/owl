import random
import engine

SYS_RANDOM = random.SystemRandom()


def _gen_token(length: int):
    return "".join(
        SYS_RANDOM.choice(
            "abcdefghilkmnopqrstuvwxyzABCDEFGHILKMNOPQRSTUVWXYZ1234567890_-+"
        )
        for _ in range(length)
    )


class SessionManager:
    active_sessions: dict[engine.IOHandle, str]
    #                     ^ handle         ^ token
    active_addr: list[str]
    player_map: dict[str, str]
    #                ^ ident ^token

    def __init__(self) -> None:
        self.active_sessions = {}
        self.player_map = {}
        self.active_addr = []

    def register_session(self, handle: engine.IOHandle) -> str:
        if handle.addr not in self.active_addr:
            token = _gen_token(32)
            self.active_sessions[handle] = token
            self.active_addr.append(handle.addr)
            return token
        else:
            for k, v in self.active_sessions.items():
                if k.addr == handle.addr:
                    return v
            else:
                raise Exception("Unreachable.")

    def link_player(self, identifier: str, handle: engine.IOHandle) -> str:
        token = self.register_session(handle)
        self.player_map[identifier] = token
        return token

    def purge(self, handle: engine.IOHandle):
        try:
            del self.active_addr[self.active_addr.index(handle.addr)]
        except ValueError:
            pass
        for ident, ptok in self.player_map.items():
            for h, stok in self.active_sessions.items():
                if stok == ptok and h.addr == handle.addr:
                    del self.player_map[ident]
                    del self.active_sessions[handle]
                    break

    async def broadcast(self, message: str):
        for handle in self.active_sessions:
            try:
                await handle.send(message)
            except ConnectionResetError:
                self.purge(handle)
