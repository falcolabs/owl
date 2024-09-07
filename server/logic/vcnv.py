from typing import override
import engine
import json
import penguin
from config import config


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

        # TODO - obfuscate this, do not give the client the answer.
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
        self.key_length = self.rpc.use_state("key_length", 69)
        self.image = self.rpc.use_state("image", "IMAGE DATA HERE")
        self.show_key = self.rpc.use_state("show_key", False)
        self.final_hint = self.rpc.use_state("final_hint", False)
        self.answers = self.rpc.use_state(
            "answers",
            [
                {"time": 29.5, "name": "MrBeast", "content": "IELT", "verdict": None},
                {"time": 1.3, "name": "Joe Biden", "content": "O-O-O", "verdict": True},
                {"time": 69.42, "name": "Trump", "content": "d4d5", "verdict": False},
                {"time": 2, "name": "herobrine", "content": "sasfsf", "verdict": None},
            ],
        )
        self.rpc.add_procedures(
            [
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
            ]
        )

    def update_tiles(
        self,
        show: engine.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        _2,
    ):
        target = call.data.args[0][1].as_str()
        new_status = call.data.args[1][1].as_str()

        mod = self.puzzle_data.get()
        # Set the required status
        if target == "M":
            mod["center"]["status"] = new_status
        else:
            for i in mod["normal"]:
                if i["tag"] == target:
                    i["status"] = new_status

        # Automatically disable others "selected" status
        # if one is selected.
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

    def verdict(
        self, _, call: engine.Packet.CallProcedure, handle: engine.IOHandle, _2
    ):
        target = call.data.args[0][1].as_str()
        verdict = json.loads(call.data.args[1][1].as_str())
        mod = self.answers.get()
        for i in mod:
            if i["name"] == target:
                i["verdict"] = verdict
        self.answers.set(mod)

    @override
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
