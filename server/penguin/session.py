import engine
from ._option import Option, Some, Null
from utils.crypt import gen_token
import traceback


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
            token = gen_token(32)
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
        engine.log_debug(f"Linked {identifier} -> {token}")
        return token

    def playername(self, token: str) -> Option[str]:
        for ident, t in self.player_map.items():
            if t == token:
                return Some(ident)
        return Null()

    def purge(self, handle: engine.IOHandle):
        try:
            del self.active_addr[self.active_addr.index(handle.addr)]
        except ValueError:
            pass

        remove_list = []
        for ident, ptok in self.player_map.items():
            for h, stok in self.active_sessions.items():
                try:
                    if stok == ptok and h.addr == handle.addr:
                        remove_list.append((ident, handle))
                        break
                # Random rust borrow checker error may occur. This is not too important.
                except Exception as e:
                    engine.log_warning(str(e))

        for ident, handle in remove_list:
            try:
                # del self.player_map[ident]
                del self.active_sessions[handle]
                engine.log_debug(f"Purged {ident}")
                # traceback.print_stack()
            except KeyError:
                pass

    async def broadcast(self, message: str):
        purgelist = []
        for handle in self.active_sessions:
            try:
                await handle.send(message)
            except ConnectionResetError as e:
                purgelist.append(handle)

        for handle in purgelist:
            self.purge(handle)
