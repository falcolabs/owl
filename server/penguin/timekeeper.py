import asyncio
import engine
from config import config

ACTIVE_CONNECTIONS: dict[str, engine.IOHandle] = {}


def on_req(raw_req: engine.RawRequest):
    ACTIVE_CONNECTIONS[raw_req.sender] = raw_req.handle


async def timekeep(time: float):
    purgelist = []
    for i, conn in ACTIVE_CONNECTIONS.items():
        try:
            await conn.send(str(time))
        except:
            purgelist.append(i)
    for i in purgelist:
        ACTIVE_CONNECTIONS.pop(i)
