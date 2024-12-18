from typing import final, override
import engine
import datetime
import penguin
from config import config
import json

STAGE_CHOOSE = 0
"""Phần chọn gói câu hỏi"""
STAGE_COMPETE = 1
"""Phần thi của thí sinh"""


@final
class VeDich(penguin.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("vedich")

        self.qdb = {
            config()
            .credentials[0]
            .username: [{20: 46, 30: 49}, {20: 47, 30: 50}, {20: 48, 30: 51}],
            config()
            .credentials[1]
            .username: [{20: 52, 30: 55}, {20: 53, 30: 56}, {20: 54, 30: 57}],
            config()
            .credentials[2]
            .username: [{20: 58, 30: 61}, {20: 59, 30: 62}, {20: 60, 30: 63}],
            config()
            .credentials[3]
            .username: [{20: 64, 30: 67}, {20: 65, 30: 68}, {20: 66, 30: 69}],
        }

        self.placement: penguin.Writable[dict[str, list[int]]] = self.rpc.use_state(
            "placement",
            {
                config().credentials[0].username: [-1, -1, -1],
                config().credentials[1].username: [-1, -1, -1],
                config().credentials[2].username: [-1, -1, -1],
                config().credentials[3].username: [-1, -1, -1],
            },
        )

        self.package = self.rpc.use_state(
            "package",
            {
                config().credentials[0].username: [0, 0, 0],
                config().credentials[1].username: [0, 0, 0],
                config().credentials[2].username: [0, 0, 0],
                config().credentials[3].username: [0, 0, 0],
            },
        )
        self.plusminus = self.rpc.use_state(
            "plusminus",
            {
                "add": [20, 30, 40, 60],
                "rem": [-30, -20, -15, -10],
            },
        )
        self.allow_bell = self.rpc.use_state("allow_bell", False)
        self.current_player_username = self.rpc.use_state("current_player_username", "")
        self.highlighted = self.rpc.use_state("highlighted", [])
        self.bell_player = self.rpc.use_state("bell_player", "")
        self.max_time = self.rpc.use_state("max_time", 15)
        self.hope_stars = self.rpc.use_state("hope_stars", [])
        self.prompt = self.rpc.use_state("prompt", "")
        self.stage = self.rpc.use_state("stage", STAGE_CHOOSE)
        self.qid = self.rpc.use_state("qid", -1)
        self.stage.subscribe(lambda _: self.qid.set(-1))
        # TODO - SECURITY: encrypt this (with MC token or sth)
        self.key = self.rpc.use_state("key", "")
        self.media = self.rpc.use_state(
            "media",
            None,
        )
        self.media_status = self.rpc.use_state(
            "media_status",
            {
                "visible": False,
                "playback_paused": False,
            },
        )
        self.rpc.add_procedures(
            [
                (
                    "set_choice",
                    self.set_choice,
                    [
                        ("target", engine.PortableType.STRING),
                        ("slot", engine.PortableType.NUMBER),
                        ("to", engine.PortableType.NUMBER),
                    ],
                ),
                (
                    "bell",
                    self.bell,
                    [
                        ("target", engine.PortableType.STRING),
                        ("clientTime", engine.PortableType.STRING),
                    ],
                ),
            ]
        )
        self.current_player_username.subscribe(
            lambda name: self.highlighted.set(
                [
                    name,
                ]
            )
        )

        self.bell_player.subscribe(
            lambda name: self.highlighted.set(
                [
                    self.current_player_username.get(),
                    name,
                ]
            )
        )
        self.qid.subscribe(self.on_qid_change)

    def on_qid_change(self, qid: int):
        if qid == -1:
            self.prompt.set("Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.")
            self.key.set("")
            return
        q = self.show.qbank.get_question(qid)
        self.prompt.set(q.prompt)
        # TODO - add configuration entry for this
        # clears bell list automatically on question change.
        self.bell_player.set("")
        self.max_time.set(q.time)
        self.key.set(q.key)
        self.show.timer.set(engine.Timer())
        if q.media is None:
            self.media.set(None)
        else:
            self.media.set(json.loads(q.media.pack()))
        self.media_status.set(
            {
                "visible": False,
                "playback_paused": False,
            }
        )

    def set_choice(
        self, _, call: engine.Packet.CallProcedure, handle: engine.IOHandle, _2
    ):
        target = call.data.str_argno(0)
        slot = call.data.int_argno(1)
        to = call.data.int_argno(2)
        try:
            c = self.package.get()
            c[target][slot] = to
            self.package.set(c)
            d = self.placement.get()
            d[target][slot] = self.qdb[target][slot][to]
            self.placement.set(d)
        except KeyError:
            engine.log_error(
                f"Unknown target/slot/to for vedich::set_choice. target={target!r}, slot={slot!r}, to={to!r}"
            )

    def bell(self, _, call: engine.Packet.CallProcedure, handle: engine.IOHandle, _2):
        target = self.session_manager.playername(call.data.str_argno(0)).unwrap()
        clientTime = call.data.str_argno(1)
        if self.bell_player.get() != "" or not self.allow_bell.get():
            engine.log_info(
                f"{target} tried to ring bell, being late to the game, or the bell is not available yet. {self.bell_player.get()}"
            )
        else:
            engine.log_info(
                f"{target} bell registered. {datetime.time().isoformat("microseconds")}"
            )
            self.show.play_sound("vedich-bell")
            self.bell_player.set(target)

    @override
    async def on_request(
        self,
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
