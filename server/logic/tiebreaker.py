from audioop import add
from typing import final, override
import engine
import penguin
from penguin import Some, Null


@final
class TieBreaker(penguin.PartImplementation):

    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("tiebreaker")

        self.question_placement = [69, 70, 71]

        self.timer = engine.Timer()
        self.timer.pause()
        self.current_question_content = self.rpc.use_state(
            "current_question_content", ""
        )
        self.plusminus = self.rpc.use_state("plusminus", {"add": [0], "rem": [0]})
        # TODO - SECURITY: encrypt this (with MC token or sth)
        self.key = self.rpc.use_state("key", "")
        self.qid = self.rpc.use_state("qid", -1)
        """Câu hỏi hiện tại."""
        self.display_qid = self.rpc.use_state("display_qid", "Chuẩn bị")
        self.max_time = self.rpc.use_state("max_time", 15)
        self.qid.subscribe(self.on_qid_change)
        self.highlighted: penguin.Writable[list[str]] = self.rpc.use_state(
            "highlighted", []
        )
        self.joint_bell = self.rpc.use_state("joint_bell", "")
        """Username thí sinh bấm chuông trả lời trong phần thi chung"""
        self.rpc.add_procedures(
            [
                (
                    "ring_bell",
                    self.ring_bell,
                    [("token", engine.PortableType.STRING)],
                ),
                ("next_question", lambda *_: self.qid.set(self.qid.get() + 1), []),
            ]
        )
        self.joint_bell.subscribe(
            lambda candidate_name: self.highlighted.set(
                self.highlighted.get()
                + [
                    candidate_name,
                ]
            )
        )

    def _joint(self, _show: penguin.Show) -> engine.Status:
        return engine.Status.RUNNING

    def ring_bell(
        self,
        show: penguin.Show,
        call: engine.Packet.CallProcedure,
        handle: engine.IOHandle,
        addr: str,
    ):
        # TODO - SECURITY: uses the addr (see rpc.py:97) to distinguish the bell ringer,
        # not the call's argument
        ringer_token = call.data.str_argno(0)
        match self.session_manager.playername(ringer_token):
            case Some(name):
                if self.joint_bell.get() == "":
                    self.joint_bell.set(name)
                    engine.log_info(f"rang the bell: {self.joint_bell.get()}")
                else:
                    engine.log_info(f"{name} ringed the bell late.")

            case Null():
                engine.log_warning(
                    f"Player with token {ringer_token}@{addr} tried to ring bell, but could not identify them. {self.session_manager.player_map}"
                )

    def on_qid_change(self, qid: int):
        if qid == -1:
            self.current_question_content.set(
                "Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút."
            )
            self.display_qid.set("Chuẩn bị")
            self.max_time.set(15)
            self.plusminus.set({"add": [0], "rem": [0]})
            self.key.set("")
            return
        q = self.show.qbank.get_question(qid)
        self.current_question_content.set(q.prompt)
        self.display_qid.set(self.question_placement.index(qid) + 1)
        self.key.set(q.key)
        self.max_time.set(q.time)
        self.plusminus.set({"add": [q.score], "rem": [q.score_false]})

        # TODO - configuration entry for this
        # automatically clearing the bell queue when question changes
        self.joint_bell.set("")
        self.highlighted.set([])
        # automatically resets timer
        self.show.timer.set(engine.Timer())

    @override
    def on_update(self, show: penguin.Show) -> engine.Status:
        # qid = self.get_qid()
        # if self.lastqid != qid and qid != -1:
        #     self.lastqid = self.get_qid()
        #     engine.log_debug(
        #         f"Setting new question content: {show.qbank.get_question(self.lastqid).prompt}"
        #     )
        #     self.set_current_question_content(
        #         show.qbank.get_question(self.lastqid).prompt
        #     )
        #     # self.set_current_question(show.qbank.get_question(self.get_qid()))
        return self._joint(show)

    @override
    async def on_request(
        self,
        show: penguin.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
