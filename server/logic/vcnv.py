from typing import override
import engine

import penguin
from config import config


class VCNV(penguin.PartImplementation):
    def __init__(self) -> None:
        super().__init__()
        self.rpc = penguin.RPCManager("vcnv")
        self.puzzle_data = self.rpc.use_state(
            "puzzle_data",
            [
                {"status": "shown", "content": "mrbeast", "tag": "1"},
                {"status": "shown", "content": "trump", "tag": "2"},
                {"status": "shown", "content": "ohio", "tag": "3"},
                {"status": "shown", "content": "しかせんべい", "tag": "4"},
            ],
        )
        self.prompt = self.rpc.use_state(
            "prompt",
            'Đây là những lời nhận xét của Hoài Thanh - Hoài Chân về ai: "chỉ tiên sinh là người của hai thế kỷ. Tiên sinh sẽ đại biểu cho một lớp người để chứng giám công việc lớp người kế tiếp. Ở địa vị ấy còn có ai xứng đáng hơn tiên sinh"?',
        )
        self.key_length = self.rpc.use_state("key_length", 69)
        self.image = self.rpc.use_state("image", "IMAGE DATA HERE")
        self.show_key = self.rpc.use_state("show_key", False)
        self.answers = self.rpc.use_state(
            "answers",
            [
                {"time": 29.5, "name": "MrBeast", "content": "IELT", "verdict": None},
                {"time": 1.3, "name": "Joe Biden", "content": "O-O-O", "verdict": True},
                {"time": 69.42, "name": "Trump", "content": "d4d5", "verdict": False},
                {"time": 2, "name": "herobrine", "content": "sasfsf", "verdict": None},
            ],
        )

    @override
    async def on_request(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ):
        (await self.rpc.handle(show, packet, handle, addr)).unwrap()
