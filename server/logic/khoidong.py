import engine
import server.utils as utils
import json
from config import config


STATE_SEPERATED = 0
"""Phần thi riêng"""
STATE_JOINT = 1
"""Phần thi chung"""


class KhoiDong(utils.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = utils.WalkieTalkie("khoidong")

        self.question_placement = {
            STATE_SEPERATED: [
                [0, 1, 2, 3, 4, 5],
                [6, 7, 8, 9, 10, 11],
                [12, 13, 14, 15, 16, 17],
                [18, 19, 20, 21, 22, 23],
            ],
            STATE_JOINT: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        }

        self.state, self.set_state = self.rpc.synced_state("state", STATE_SEPERATED)
        """Trạng thái phần thi."""
        self.qid, self.set_qid = self.rpc.synced_state("qid", -1)
        self.lastqid = self.qid()
        """Trạng thái phần thi."""
        self.seperated_candidate, self.set_seperated_candidate = self.rpc.synced_state(
            "seperated_candidate", ""
        )
        self.current_question, self.set_current_question = self.rpc.synced_state("current_question", engine.Question("", "", 0, [], 0, ""))
        """Lượt thi của thí sinh trong phần thi riêng"""
        self.joint_bell, self.set_joint_bell = self.rpc.synced_state("joint_bell", "")
        """Thí sinh bấm chuông trả lời trong phần thi chung"""
        self.rpc.add_procedures(
            [
                (
                    "setstate_seperated",
                    lambda *_: self.set_state(STATE_SEPERATED),
                ),
                (
                    "setstate_joint",
                    lambda *_: self.set_state(STATE_JOINT),
                ),
                (
                    "set_seperated_candidate",
                    lambda _, callprod, _3, _4: self.set_seperated_candidate(json.loads(callprod.data.args()[0][1])),
                )
            ]
        )

    def _seperated(self, show: engine.Show) -> engine.Status:
        qid = self.qid()
        if self.lastqid != qid and qid != -1:
            self.lastqid = self.qid()
            self.set_current_question(show.qbank.get_question(self.qid()))

        return engine.Status.RUNNING

    def _joint(self, show: engine.Show) -> engine.Status:
        
        return engine.Status.RUNNING

    def on_update(self, show: engine.Show) -> engine.Status:
        if self.state == STATE_SEPERATED:
            return self._seperated(show)
        return self._joint(show)

    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        await self.rpc.handle(show, packet, handle, addr)
