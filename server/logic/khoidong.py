from typing import override
import engine
import penguin

STAGE_SEPERATED = 0
"""Phần thi riêng"""
STAGE_JOINT = 1
"""Phần thi chung"""


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
            STAGE_JOINT: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        }

        self.timer = engine.Timer()
        self.timer.pause()

        self.state = self.rpc.use_state("stage", STAGE_SEPERATED)
        """Trạng thái phần thi."""
        self.current_question_content = self.rpc.use_state(
            "current_question_content", ""
        )
        """Username của thí sinh lượt thi hiện tại trong phần thi riêng"""
        self.qid = self.rpc.use_state("qid", -1)
        """Câu hỏi hiện tại."""
        self.qid.subscribe(self.on_qid_change)

        self.seperated_candidate = self.rpc.use_state("seperated_candidate", "")
        self.joint_bell = self.rpc.use_state("joint_bell", "")
        """Username thí sinh bấm chuông trả lời trong phần thi chung"""
        self.rpc.add_procedures(
            [
                ("setstage_seperated", lambda *_: self.state.set(STAGE_SEPERATED), []),
                ("setstage_joint", lambda *_: self.state.set(STAGE_JOINT), []),
                (
                    "ring_bell",
                    lambda _, callprod, _2, _3: self.joint_bell.set(
                        callprod.data.args[0][1].as_str()
                    ),
                    [],
                ),
                ("next_question", lambda *_: self.qid.set(self.qid.get() + 1), []),
            ]
        )

    def _seperated(self, _show: engine.Show) -> engine.Status:
        return engine.Status.RUNNING

    def _joint(self, _show: engine.Show) -> engine.Status:
        return engine.Status.RUNNING

    def on_qid_change(self, _: engine.PortableValue):
        if self.qid.get() == -1:
            self.current_question_content.set(
                "Thí sinh hãy chuẩn bị. Phần thi sẽ bắt đầu trong ít phút."
            )
            return
        self.current_question_content.set(
            penguin.SHOW.qbank.get_question(self.qid.get()).prompt
        )

    @override
    def on_update(self, show: engine.Show) -> engine.Status:
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
        if self.state.get() == STAGE_SEPERATED:
            return self._seperated(show)
        return self._joint(show)

    @override
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
