from typing import final, override
import engine
import json
from penguin import Some, Null
import utils.vcnv
import penguin
from config import config
import datetime
import time
import typing


class PlayerAnswer(typing.TypedDict):
    time: float
    name: str
    content: str
    verdict: bool


@final
class VCNV(penguin.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("vcnv")
        self.sel2qidmap = {
            "1": 36,
            "2": 37,
            "3": 38,
            "4": 38,
            "M": 40,
        }

        self.DEFAULT_ANSWERS: list[PlayerAnswer] = []

        # TODO - SECURITY: obfuscate this, do not give the client the answer.
        self.puzzle_data = self.rpc.use_state(
            "puzzle_data",
            {
                "normal": [
                    {"status": "hidden", "content": "mrbeast", "tag": "1"},
                    {"status": "hidden", "content": "trump", "tag": "2"},
                    {"status": "hidden", "content": "ohio", "tag": "3"},
                    {"status": "hidden", "content": "しかせんべい", "tag": "4"},
                ],
                "center": {"status": "hidden", "content": "mrbeast", "tag": "M"},
            },
        )
        self.prompt = self.rpc.use_state(
            "prompt",
            "Thí sinh hãy chọn một hàng ngang.",
        )
        self.selected = self.rpc.use_state("selected", "")
        self.highlighted: penguin.Writable[list[str]] = self.rpc.use_state(
            "highlighted", []
        )
        self.plusminus = self.rpc.use_state("plusminus", {"add": [10], "rem": [0]})
        self.key_length = self.rpc.use_state("key_length", 69)
        self.image = self.rpc.use_state(
            "image", utils.vcnv.get_imgdata(["1", "2", "3", "4", "M"])
        )
        self.show_key = self.rpc.use_state("show_key", False)
        self.max_time = self.rpc.use_state("max_time", 15)
        self.final_hint = self.rpc.use_state("final_hint", False)
        self.answers: penguin.Writable[list[PlayerAnswer]] = self.rpc.use_state(
            "answers",
            [],
        )
        self.rpc.add_procedures(
            [
                (
                    "submit_answer",
                    self.submit_answer,
                    [
                        ("answer", engine.PortableType.STRING),
                        ("token", engine.PortableType.STRING),
                        ("time", engine.PortableType.NUMBER),
                    ],
                ),
                (
                    "update_tiles",
                    self.update_tiles,
                    [
                        ("target", engine.PortableType.STRING),
                        ("status", engine.PortableType.STRING),
                    ],
                ),
                (
                    "verdict",
                    self.verdict,
                    [
                        ("target", engine.PortableType.STRING),
                        ("verdict", engine.PortableType.STRING),
                    ],
                ),
                (
                    "bell",
                    self.bell,
                    [
                        ("token", engine.PortableType.STRING),
                        ("timeMs", engine.PortableType.NUMBER),
                    ],
                ),
            ]
        )

    @override
    def on_ready(self, show: penguin.Show):
        self.DEFAULT_ANSWERS = [
            {"time": 30, "name": p.identifier, "content": "", "verdict": False}
            for p in show.players.get()
        ]

    def submit_answer(
        self,
        show: penguin.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        addr,
    ):
        answer, token, time = (
            call.data.str_argno(0),
            call.data.str_argno(1),
            call.data.float_argno(2),
        )
        print(self.show.session_manager.player_map)
        match self.show.session_manager.playername(token):
            case Some(name):
                elapsed: float = self.show.timer.get().time_elapsed().total_seconds()
                engine.log_info(
                    f"Timing mismatch report: client: {time:.4f}, server:{elapsed:.4f}, delta: ±{abs(elapsed-time):.4f}"
                )
                anslist = self.answers.get()
                output = anslist.copy()
                for i, a in enumerate(anslist):
                    if a["name"] == name:
                        output[i] = {  # type: ignore[reportArgumentType]
                            "time": elapsed,
                            "name": name,
                            "content": answer,
                            "verdict": False,
                        }
                        break
                else:
                    output.append(
                        {
                            "time": elapsed,
                            "name": name,
                            "content": answer,
                            "verdict": False,
                        }
                    )
                self.answers.set(output)
            case Null():
                engine.log_warning(
                    f"Unidentified player {token}@{addr} tried to submit answer. Ignored."
                )

    def update_tiles(
        self,
        show: penguin.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        _2,
    ):
        target = call.data.str_argno(0)
        new_status = call.data.str_argno(1)
        # TODO - make a configuration value for this
        # Automatically clears the answer queue on changing tile state
        self.answers.set(self.DEFAULT_ANSWERS)
        # Automatically clears the bell list on changing tile state
        self.highlighted.set([])

        mod = self.puzzle_data.get()
        # Set the required status
        if target == "M":
            mod["center"]["status"] = new_status
        else:
            for i in mod["normal"]:
                if i["tag"] == target:
                    i["status"] = new_status

        # Automatically disable others' "selected" status
        # if one of them is selected.
        if new_status == "selected":
            for i in mod["normal"]:
                if i["status"] == "selected" and i["tag"] != target:
                    i["status"] = "hidden"
            if target != "M" and mod["center"]["status"] == "selected":
                mod["center"]["status"] = "hidden"

        # Set selected variable
        for i in mod["normal"] + [mod["center"]]:
            if i["status"] == "selected":
                self.selected.set(i["tag"])
                self.prompt.set(show.qbank.get_question(self.sel2qidmap[target]).prompt)
                break
        else:
            self.selected.set("")
            self.prompt.set("Thí sinh hãy lựa chọn hàng ngang.")
        self.puzzle_data.set(mod)
        self.image.set(
            utils.vcnv.get_imgdata(
                [
                    "1" if mod["normal"][0]["status"] != "shown" else "",
                    "2" if mod["normal"][1]["status"] != "shown" else "",
                    "3" if mod["normal"][2]["status"] != "shown" else "",
                    "4" if mod["normal"][3]["status"] != "shown" else "",
                    "M" if mod["center"]["status"] != "shown" else "",
                ]
            )
        )

    def verdict(
        self, _, call: engine.Packet.CallProcedure, handle: engine.IOHandle, _2
    ):
        target = call.data.str_argno(0)
        verdict = json.loads(call.data.str_argno(1))
        mod = self.answers.get()
        for i in mod:
            if i["name"] == target:
                i["verdict"] = verdict
        self.answers.set(mod)

    def bell(self, _, call: engine.Packet.CallProcedure, handle: engine.IOHandle, _2):
        target = call.data.str_argno(0)
        # TODO - check timeMs also
        engine.log_info(
            f"{target} pressed bell on {datetime.time().isoformat("microseconds")}"
        )
        bell_list = self.highlighted.get()
        bell_list.insert(0, target)
        self.highlighted.set(bell_list)

    @override
    async def on_request(
        self,
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
