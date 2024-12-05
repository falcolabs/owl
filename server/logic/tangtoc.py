from typing import final, override
import engine
import json
import penguin
from config import config
import typing
from penguin import Some, Null


class PlayerAnswer(typing.TypedDict):
    time: float
    name: str
    content: str
    verdict: bool


@final
class TangToc(penguin.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("tangtoc")
        self.qid = self.rpc.use_state("qid", -1)
        # TODO - SECURITY: encrypt this
        self.key = self.rpc.use_state("key", "")
        self.preload_list = self.rpc.use_state("preload_list", {})
        self.prompt = self.rpc.use_state(
            "prompt",
            "Các thí sinh hãy chuẩn bị",
        )
        self.highlighted = self.rpc.use_state("highlighted", [])
        self.DEFAULT_ANSWERS: list[PlayerAnswer] = []
        self.media = self.rpc.use_state(
            "media",
            None,
        )
        self.allow_input = self.rpc.use_state("allow_input", False)

        self.plusminus = self.rpc.use_state(
            "plusminus", {"add": [10, 20, 30, 40], "rem": [0]}
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
            [],
        )
        self.max_time = self.rpc.use_state("max_time", -1)
        self.qid.subscribe(self.on_qid_change)
        self.rpc.add_procedures(
            [
                (
                    "submit_answer",
                    self.submit_answer,
                    [
                        ("answer", engine.PortableType.STRING),
                        ("token", engine.PortableType.STRING),
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

    def submit_answer(
        self,
        show: penguin.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        addr,
    ):
        answer, token = (
            call.data.str_argno(0),
            call.data.str_argno(1),
        )
        match self.show.session_manager.playername(token):
            case Some(name):
                elapsed: float = self.show.timer.get().time_elapsed().total_seconds()
                anslist = self.answers.get()
                output = anslist.copy()
                for i, a in enumerate(anslist):
                    if a["name"] == name:
                        output[i] = {
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
                output = sorted(output, key=lambda x: x["time"])
                self.answers.set(output)
            case Null():
                engine.log_warning(
                    f"Unidentified player {token}@{addr} tried to submit answer. Ignored."
                )

    @override
    def on_ready(self, show: penguin.Show):
        a, b, c, d = (
            show.qbank.get_question(42).media,
            show.qbank.get_question(43).media,
            show.qbank.get_question(44).media,
            show.qbank.get_question(45).media,
        )
        self.show.timer.subscribe(lambda t: self.allow_input.set(not t.is_paused))

        self.preload_list.set(
            {
                41: a.pack() if a is not None else None,
                42: b.pack() if b is not None else None,
                43: c.pack() if c is not None else None,
                44: d.pack() if d is not None else None,
            }
        )
        self.DEFAULT_ANSWERS = [
            {"time": 30, "name": p.identifier, "content": "", "verdict": False}
            for p in show.players.get()
        ]
        self.answers.set(self.DEFAULT_ANSWERS)

    def on_qid_change(self, qid: int):
        if qid == -1:
            self.prompt.set("Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.")
            self.media.set({"media_type": None, "uri": None})
            self.key.set("")
            return
        q = self.show.qbank.get_question(qid)
        self.prompt.set(q.prompt)
        self.answers.set(self.DEFAULT_ANSWERS)
        self.show_key.set(False)
        self.max_time = self.rpc.use_state("max_time", q.time)
        self.key.set(q.key)
        self.show.timer.set(engine.Timer())
        if q.media is None:
            self.media.set(None)
        else:
            self.media.set(json.loads(q.media.pack()))

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

    @override
    async def on_request(
        self,
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
