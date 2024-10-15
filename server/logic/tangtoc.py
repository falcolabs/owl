from typing import override
import engine
import json
import penguin
from config import config


class TangToc(penguin.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("tangtoc")
        self.qid = self.rpc.use_state("qid", -1)
        self.prompt = self.rpc.use_state(
            "prompt",
            "Sắp xếp các hình minh họa vào vị trí tương ứng để hoàn thiện sơ đồ quá trình nguyên phân ở tế bào động vật",
        )
        self.media = self.rpc.use_state(
            "media",
            None,
        )

        self.media_status = self.rpc.use_state(
            "media_status",
            {
                "visible": True,
                "playback_paused": True,
            },
        )
        self.show_key = self.rpc.use_state(
            "show_key",
            False,
        )
        self.answers = self.rpc.use_state(
            "answers",
            [
                {"time": 29.5, "name": "MrBeast", "content": "IELT", "verdict": None},
                {"time": 1.3, "name": "Joe Biden", "content": "O-O-O", "verdict": True},
                {"time": 69.42, "name": "Trump", "content": "d4d5", "verdict": False},
                {"time": 2, "name": "herobrine", "content": "sasfsf", "verdict": None},
            ],
        )
        self.qid.subscribe(self.on_qid_change)
        self.rpc.add_procedures(
            [
                (
                    "verdict",
                    self.verdict,
                    [
                        ("target", engine.PortableType.STRING),
                        ("verdict", engine.PortableType.STRING),
                    ],
                )
            ]
        )

    def on_qid_change(self, qid: int):
        if qid == -1:
            self.prompt.set("Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.")
            self.media.set({"media_type": None, "uri": None})
            return
        q = penguin.SHOW.qbank.get_question(qid)
        self.prompt.set(q.prompt)
        if q.media is None:
            self.media.set(None)
        else:
            self.media.set(json.loads(q.media.pack()))

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
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
