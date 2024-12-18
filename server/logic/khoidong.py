from audioop import add
from typing import final, override
import engine
import penguin
from penguin import Some, Null

STAGE_SEPERATED = 0
"""Phần thi riêng"""
STAGE_JOINT = 1
"""Phần thi chung"""


@final
class KhoiDong(penguin.PartImplementation):

    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("khoidong")

        self.question_placement = {
            STAGE_SEPERATED: {
                0: [0, 1, 2, 3, 4, 5],
                1: [6, 7, 8, 9, 10, 11],
                2: [12, 13, 14, 15, 16, 17],
                3: [18, 19, 20, 21, 22, 23],
            },
            STAGE_JOINT: [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
        }
        self.timer = engine.Timer()
        self.timer.pause()
        self.allow_bell = self.rpc.use_state("allow_bell", False)
        self.stage = self.rpc.use_state("stage", STAGE_SEPERATED)
        """Trạng thái phần thi."""
        self.prompt = self.rpc.use_state("prompt", "")
        # TODO - SECURITY: encrypt this
        self.key = self.rpc.use_state("key", "")
        self.plusminus = self.rpc.use_state("plusminus", {"add": [0], "rem": [0]})
        self.qid = self.rpc.use_state("qid", -1)
        """Câu hỏi hiện tại."""
        self.display_qid = self.rpc.use_state("display_qid", "Chuẩn bị")
        self.max_time = self.rpc.use_state("max_time", 3)
        self.qid.subscribe(self.on_qid_change)
        self.highlighted: penguin.Writable[list[str]] = self.rpc.use_state(
            "highlighted", []
        )
        self.seperated_candidate = self.rpc.use_state("seperated_candidate", "")
        """Username của thí sinh lượt thi hiện tại trong phần thi riêng"""
        self.joint_bell = self.rpc.use_state("joint_bell", "")
        """Username thí sinh bấm chuông trả lời trong phần thi chung"""
        self.rpc.add_procedures(
            [
                ("setstage_seperated", lambda *_: self.stage.set(STAGE_SEPERATED), []),
                ("setstage_joint", lambda *_: self.stage.set(STAGE_JOINT), []),
                (
                    "ring_bell",
                    self.ring_bell,
                    [("token", engine.PortableType.STRING)],
                ),
                ("next_question", lambda *_: self.qid.set(self.qid.get() + 1), []),
            ]
        )
        self.seperated_candidate.subscribe(
            lambda candidate_name: self.highlighted.set(
                [
                    candidate_name,
                ]
            )
        )
        self.joint_bell.subscribe(
            lambda candidate_name: self.highlighted.set(
                [
                    candidate_name,
                ]
            )
        )

        # Resets the highlighted list when game stage is changed.
        self.stage.subscribe(lambda _: self.highlighted.set([]))
        self.stage.subscribe(lambda _: self.qid.set(-1))

    def _seperated(self, _show: penguin.Show) -> engine.Status:
        return engine.Status.RUNNING

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
        if not self.allow_bell.get():
            return
        match self.session_manager.playername(ringer_token):
            case Some(name):
                if self.joint_bell.get() == "":
                    self.show.play_sound("khoidong-bell")
                    self.joint_bell.set(name)
                    engine.log_info(f"rang the bell: {self.joint_bell.get()}")
                else:
                    engine.log_info(f"{name} ringed the bell late.")

            case Null():
                engine.log_warning(
                    f"Player with token {ringer_token}@{addr} tried to ring bell, but could not identify them. {self.session_manager.player_map}"
                )

    def on_qid_change(self, qid: int):
        self.allow_bell.set(False)
        if qid == -1:
            self.prompt.set("Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút.")
            self.display_qid.set("Chuẩn bị")
            self.key.set("")
            self.max_time.set(3)
            self.plusminus.set({"add": [0], "rem": [0]})
            return
        q = self.show.qbank.get_question(qid)
        self.prompt.set(q.prompt)
        if self.stage.get() == STAGE_SEPERATED:
            self.display_qid.set(str((qid % 6) + 1))
        else:
            self.display_qid.set(self.question_placement[STAGE_JOINT].index(qid) + 1)  # type: ignore[reportAttributeAccessIssue]

        self.max_time.set(q.time)
        self.plusminus.set({"add": [q.score], "rem": [q.score_false]})
        self.key.set(q.key)

        # TODO - configuration entry for this
        # automatically clearing the bell queue when question changes
        self.joint_bell.set("")
        if self.stage.get() == STAGE_SEPERATED:
            self.highlighted.set(
                [
                    self.seperated_candidate.get(),
                ]
            )
        else:
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
        #     self.set_prompt(
        #         show.qbank.get_question(self.lastqid).prompt
        #     )
        #     # self.set_current_question(show.qbank.get_question(self.get_qid()))
        if self.stage.get() == STAGE_SEPERATED:
            return self._seperated(show)
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
