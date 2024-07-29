from typing import Any, Optional, Callable, Literal, Union, Iterable, Mapping
from abc import abstractmethod, ABC

PacketData = Union[
    AuthenticationStatus,
    PartProperties,
    Player,
    Credentials,
    Question,
    QuestionBank,
    ResourceRequest,
    Show,
    Ticker,
    Timer,
    str,
    list[Procedure],
    ProcedureCall,
    GameStateUpdate,
    GameStateValue,
]

class Packet(ABC):
    """An object encapsulating data decoded from JSON."""

    class AuthStatus(Packet):
        data: AuthenticationStatus
        def __init__(self, data: AuthenticationStatus): ...

    class Part(Packet):
        data: PartProperties
        def __init__(self, data: PartProperties): ...

    class Player(Packet):
        data: Player
        def __init__(self, data: Player): ...

    class CommenceSession(Packet):
        data: Credentials
        def __init__(self, data: Credentials): ...

    class Question(Packet):
        data: Question
        def __init__(self, data: Question): ...

    class QuestionBank(Packet):
        data: QuestionBank
        def __init__(self, data: QuestionBank): ...

    class RequestResource(Packet):
        data: ResourceRequest
        def __init__(self, data: ResourceRequest): ...

    class Show(Packet):
        data: Show
        def __init__(self, data: Show): ...

    class Ticker(Packet):
        data: Ticker
        def __init__(self, data: Ticker): ...

    class Timer(Packet):
        data: Timer
        def __init__(self, data: Timer): ...

    class ProcedureList(Packet):
        data: list[Procedure]
        def __init__(self, data: list[Procedure]): ...

    class CallProcedure(Packet):
        data: ProcedureCall
        def __init__(self, data: ProcedureCall): ...

    class GameState(Packet):
        data: GameStateValue
        def __init__(self, data: GameStateValue): ...

    class UpdateGameState(Packet):
        data: GameStateUpdate
        def __init__(self, data: GameStateUpdate): ...

    class Unknown(Packet):
        data: str
        def __init__(self, data: str): ...

    data: PacketData

    @abstractmethod
    def __init__(self, data: PacketData): ...
    def __str__(self) -> str: ...
    def pack(self) -> str: ...

PortableValueName = (
    Literal["array"]
    | Literal["null"]
    | Literal["number"]
    | Literal["string"]
    | Literal["object"]
)

class PortableValueType:
    ARRAY = 0
    NUMBER = 1
    STRING = 2
    NULL = 3
    OBJECT = 4
    BOOLEAN = 5

class PortableValue:
    def __init__(self, data: str, type: PortableValueType): ...
    def as_str(self) -> str: ...
    def as_int(self) -> int: ...
    def as_float(self) -> float: ...
    def data(self) -> str: ...
    def data_type(self) -> PortableValueType: ...

class Procedure:
    def __init__(
        self, name: str, hidden: bool, args: list[tuple[str, PortableValueType]]
    ): ...
    def name(self) -> str: ...
    def hidden(self) -> bool: ...

class ProcedureCall:
    def name(self) -> str: ...
    def args(self) -> list[tuple[str, PortableValue]]: ...

class GameStateValue:
    def __init__(self, name: str, hidden: bool, data_type: PortableValue): ...
    def name(self) -> str: ...
    def hidden(self) -> bool: ...

class GameStateUpdate:
    def name(self) -> str: ...
    def data(self) -> PortableValue: ...

class Show:
    """The name of the show."""

    name: str
    """The parts included in the show."""
    parts: list[Part]
    """The show's tick speed."""
    tick_speed: int
    """The current part index."""
    current_part: int
    """The players present"""
    players: list[Player]
    """All the questions the show contains"""
    qbank: QuestionBank
    """The show's ticker"""
    ticker: Ticker
    """The show's timer"""
    timer: Timer

    def __init__(
        self,
        name: str,
        parts: list[Part],
        players: list[Player],
        tick_speed: int,
        question_bank: QuestionBank,
    ): ...
    @abstractmethod
    def start(
        self,
        listen_on: str,
        serve_on: str,
        static_dir: str,
    ):
        """
        Starts the show. This is a blocking function, and will only stop
        when the show is terminated by the user.

        # Arguments
        * `listen_on` - the host and port for the server to listen on.
                        resource will be hosted on `/`, WebSocket PI on `/harlem`
        * `serve_dir` - where the static content will be hosted at.
                        May contain unsolicited WebAssembly.
        * `static_dir` - where the static content lives. Should contain `404.html`.

        # Examples
        ```py
        # This function will block until the show ends.
        show.start("localhost:6942", "./public", "./static")
        ```
        """

    @staticmethod
    def ws_task(
        listen_on: str,
        serve_on: str,
        static_dir: str,
        call_hook: Callable[[RawRequest], None],
    ): ...

class RawRequest:
    handle: IOHandle
    sender: str
    content: Packet

class IOHandle:
    async def send(self, msg: str): ...

class Status:
    RUNNING: Status
    """Running as usual."""
    SKIP: Status
    """Skipping the current part and jump on the next part."""
    REWIND: Status
    """Stopping the current part and returning to the previous one."""
    PAUSED: Status
    """Pause the current part."""
    STOP: Status
    """The show is stopping."""

class Part:
    props: PartProperties
    implementation: PartImplementation

    def __init__(self, wrapped: object, name: str): ...

class PartImplementation(ABC):
    def on_update(self, show: Show) -> Status: ...
    async def on_request(
        self,
        show: Show,
        packet: Packet,
        handle: IOHandle,
        addr: str,
    ): ...

class PartProperties:
    name: str
    def __init__(self, name: str) -> None: ...

class Player:
    identifier: str
    name: str
    score: int

    def __init__(self, identifier: str, name: str, score: int) -> None: ...
    def add_score(self, additional_score: int) -> int: ...
    def handle(self) -> IOHandle: ...
    def set_handle(self, handle: IOHandle) -> None: ...

class Question:
    prompt: str
    key: str
    score: int
    choices: Optional[list[str]]
    score_false: Optional[int]
    explaination: Optional[str]

    def __init__(
        self,
        prompt: str,
        key: str,
        score: int,
        choices: list[str],
        score_false: int,
        explaination: str,
    ): ...

class QuestionBank:
    question_storage: list[Question]

    def load(self, filepath: str) -> None:
        """
        Load questions from a JSON file and stores it.
        It should have the following structure:
        ```json
        [
        {
            "prompt": "What is one plus one?",
            "key": "Two",
            "score": 100,
            // Optional properties
            "choices": ["One", "Two", "Three", "One Million Five Hundred and Fifty Two Thousand Seven Hundred and Three"],
            "score_false": -5,
            "explaination": "bruh"
        },
        ...
        ]
        ```
        """

    def get_question(self, qid: int) -> Question:
        """Gets the question with the specified ID.
        Will panic if no questions with the specified ID exists."""

    def random_question(self) -> Question:
        """Gets a random question.
        Panics if there are no questions in the bank."""

    def random_n_questions(self, n: int) -> list[Question]:
        """Gets a specified number of unique random questions.
        Panics if there are no questions in the bank."""

class Timer:
    start_time: Any
    paused_time: Any
    paused_duration: Any
    is_paused: bool

    def __init__(self):
        """Creates a new timer, which starts immidiately after creation."""

    def pause(self) -> None:
        """Pauses the timer."""

    def resume(self) -> None:
        """Resumes the timer."""

    def time_elapsed(self) -> Any:
        """Gets the time elapsed from the calling of `start()`,
        minus the pauses."""

class Ticker:
    last_tick: Any

    def tick(self, tick_speed: int):
        """Ensures the tick speed is met."""

class Credentials:
    username: str
    access_key: str

class AuthenticationStatus:
    success: bool
    message: str

    def __init__(self, success: bool, message: str): ...

# = Union[
#     ResourceRequest.Player,
#     ResourceRequest.Question,
#     ResourceRequest.QuestionBank,
#     ResourceRequest.Show,
#     ResourceRequest.Ticker,
#     ResourceRequest.Timer,
#     ResourceRequest.CurrentPart,
# ]

class ResourceRequest(ABC):
    class Player(ResourceRequest):
        index: str
        def __init__(self, index: str): ...

    class Question(ResourceRequest):
        index: int
        def __init__(self, index: int): ...

    class PartByID(ResourceRequest):
        index: int
        def __init__(self, index: int): ...

    class PartByName(ResourceRequest):
        index: str
        def __init__(self, index: str): ...

    class QuestionBank(ResourceRequest):
        pass

    class Show(ResourceRequest):
        pass

    class Ticker(ResourceRequest):
        pass

    class Timer(ResourceRequest):
        pass

    class CurrentPart(ResourceRequest):
        pass

    class AvailableProcedures(ResourceRequest):
        pass

    class GameState(ResourceRequest):
        pass

class Color:
    BLACK: Color
    RED: Color
    GREEN: Color
    YELLOW: Color
    BLUE: Color
    MAGENTA: Color
    CYAN: Color
    WHITE: Color
    BRIGHT_BLACK: Color
    GRAY: Color
    GREY: Color
    BRIGHT_RED: Color
    BRIGHT_GREEN: Color
    BRIGHT_YELLOW: Color
    BRIGHT_BLUE: Color
    BRIGHT_MAGENTA: Color
    BRIGHT_CYAN: Color
    BRIGHT_WHITE: Color
    RESET: Color
    BOLD: Color
    UNDERLINE: Color
    REVERSED: Color
    BLANK: Color

    def to_string(self) -> str: ...

class Level:
    DEBUG: Level
    SUCCESS: Level
    INFO: Level
    WARNING: Level
    ERROR: Level

    def get_color(self) -> Color: ...
    def get_prio(self) -> int: ...
    def get_name(self) -> str: ...

def to_color(color: str) -> Color: ...
def mccolor(text: str) -> str: ...
def mccolor_esc(text: str, esc_char: str) -> str: ...
def log_debug(content: str): ...
def log_success(content: str): ...
def log_info(content: str): ...
def log_warning(content: str): ...
def log_error(content: str): ...
