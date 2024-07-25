import engine
import pengin
from config import config

STATE_SEPERATED = 0
"""Phần thi riêng"""
STATE_JOINT = 1
"""Phần thi chung"""


class KhoiDong(pengin.PartImplementation):
    def __init__(self) -> None:
        self.state: int = 0
        """Trạng thái phần thi."""
        self.seperated_candidate: int = 0
        """Lượt thi của thí sinh trong phần thi riêng"""
        self.joint_bell: int = 0
        """Thí sinh bấm chuông trả lời trong phần thi chung"""
        super().__init__()

    def _seperated(self, show: engine.Show) -> engine.Status:
        



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
        pass
