import datetime
from typing import (
    Any,
    Dict,
    Optional,
    Callable,
    Literal,
    Union,
    Iterable,
    Mapping,
    override,
)
from warnings import deprecated  # type: ignore[reportAttributeAccessIssue]
from abc import abstractmethod, ABC

PacketData = (
    AuthenticationStatus
    | PartProperties
    | Player
    | Credentials
    | Question
    | QuestionBank
    | Query
    | Ticker
    | Timer
    | str
    | list[ProcedureSignature]
    | ProcedureCall
    | GameState
    | list[GameState]
)
"""All the possible values in a packet's data."""

class Packet(ABC):
    """An algebraic datatype encapsulating data, serialize and
    deserializable to and from JSON. Only `serde@rust` may
    deserialize a `Packet`, while serializing is available
    everywhere using `.pack()` or `str()`.

    ---
    Available on: ✓ Python, ✓ Rust, ✗ JavaScript, ✓ WASM

    For JavaScript, please use the `ClientPacket` API.

    ---
    ### Usage
    A `match` statement may be used to differentiate between these
    variants:
    ```python
    match packet:
        case Packet.AuthStatus():
            ...
        case _:
            ...
    ```
    You may also use `isinstance()`:
    ```python
    if isinstance(x, Packet.AuthStatus):
        ...
    ```
    """

    class AuthStatus(Packet):
        """An :class:`AuthStatus` packet is sent to announce
        to the client the success or failure of a :class:`Packet.CommenceSession`."""

        data: AuthenticationStatus
        def __init__(self, data: AuthenticationStatus): ...

    class Part(Packet):
        """A :class:`Packet` contains properties about a game's part."""

        data: PartProperties
        def __init__(self, data: PartProperties): ...

    class Player(Packet):
        """A :class:`Player` contains information about a given player."""

        data: Player
        def __init__(self, data: Player): ...

    class CommenceSession(Packet):
        """This packet is sent in order to initiate connection between the
        server and the client. API will change in order to implement security
        measures.
        """

        data: Credentials
        def __init__(self, data: Credentials): ...

    class Question(Packet):
        """A packet containing a signle question."""

        data: Question
        def __init__(self, data: Question): ...

    class QuestionBank(Packet):
        """A packet containing an entire question database."""

        data: QuestionBank
        def __init__(self, data: QuestionBank): ...

    class Query(Packet):
        """A packet containing a query for the resource specified in its payload.
        The server is to respond by sending the correct packet type to the client."""

        data: Query
        def __init__(self, data: Query): ...

    class Ticker(Packet):
        """A packet containing a `Ticker`. See :class:`Ticker` for more details."""

        data: Ticker
        def __init__(self, data: Ticker): ...

    class Timer(Packet):
        """A packet containing a `Timer`. See :class:`Timer` for more details."""

        data: Timer
        def __init__(self, data: Timer): ...

    class ProcedureList(Packet):
        """A packet listing all of the available procedures the part can execute."""

        data: list[ProcedureSignature]
        def __init__(self, data: list[ProcedureSignature]): ...

    class CallProcedure(Packet):
        """A packet invoking the procedure."""

        data: ProcedureCall
        def __init__(self, data: ProcedureCall): ...

    class StateList(Packet):
        """A packet containing a list of all states present."""

        data: list[GameState]
        def __init__(self, data: list[GameState]): ...

    class State(Packet):
        """A packet containing a paticular state of the game."""

        data: GameState
        def __init__(self, data: GameState): ...

    class UpdateState(Packet):
        """A packet updating the state of the game."""

        data: GameState
        def __init__(self, data: GameState): ...

    class Unknown(Packet):
        """An packet used to contain unknown data."""

        data: str
        def __init__(self, data: str): ...

    class PlayerList(Packet):
        """Packet containing a list of players."""

        data: list[Player]
        def __init__(self, data: list[Player]): ...

    class PartList(Packet):
        """Packet containing a list of players."""

        data: list[PartProperties]
        def __init__(self, data: list[PartProperties]): ...

    class PlaySound(Packet):
        """Packet containing a list of players."""

        data: list[Player]
        def __init__(self, data: str): ...

    class NextAnimation(Packet):
        """Packet containing a list of players."""

        data: list[Player]
        def __init__(self, data: str): ...

    data: PacketData

    @abstractmethod
    def __init__(self, data: PacketData): ...
    @override
    def __str__(self) -> str: ...
    def pack(self) -> str: ...

class PortableType:
    """All of the types representable in a :class:`PortableValue`."""

    ARRAY: PortableType
    NUMBER: PortableType
    STRING: PortableType
    NULL: PortableType
    OBJECT: PortableType
    BOOLEAN: PortableType

class PortableValue:
    """A JSON-serialized value that may be sent and received as
    arguments for :class:`ProcedureCall`, or value for :class:`GameStateUpdate`
    ---
    Available on: ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM"""

    json: str
    data_type: PortableType

    def __init__(self, json: str, data_type: PortableType): ...
    def as_str(self) -> str: ...
    def as_int(self) -> int: ...
    def as_float(self) -> float: ...

class ProcedureSignature:
    """The signature for a procedure.

    ---
    Available on: ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    name: str
    hidden: bool

    def __init__(
        self, name: str, hidden: bool, args: list[tuple[str, PortableType]]
    ): ...

class ProcedureCall:
    """A procedure call.

    ---
    Available on: ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    name: str
    args: list[tuple[str, PortableValue]]

    def argno(self, n: int) -> PortableValue:
        """Returns the argument with the provided index.

        :param n: the index of the argument.
        :return: the argument at said index.
        """

    def argname(self, n: str) -> PortableValue:
        """Returns the argument with the provided name.

        :param n: the name of the argument.
        :return: the argument at said name.
        """

    def str_argno(self, n: int) -> str:
        """Returns the argument with the provided index.

        :param n: the index of the argument.
        :return: the argument at said index casted to `str`.
        """

    def int_argno(self, n: int) -> int:
        """Returns the argument with the provided index.

        :param n: the index of the argument.
        :return: the argument at said index casted to `int`.
        """

    def float_argno(self, n: int) -> float:
        """Returns the argument with the provided index.

        :param n: the index of the argument.
        :return: the argument at said index casted to `float`.
        """

    def str_arg(self, n: str) -> str:
        """Returns the argument with the provided name.

        :param n: the name of the argument.
        :return: the argument at said name casted to `str`.
        """

    def int_arg(self, n: str) -> int:
        """Returns the argument with the provided name.

        :param n: the name of the argument.
        :return: the argument at said name casted to `int`.
        """

    def float_arg(self, n: str) -> float:
        """Returns the argument with the provided name.

        :param n: the name of the argument.
        :return: the argument at said name casted to `float`.
        """

class GameState:
    """
    A game state.

    Available on: ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM"""

    name: str
    data: PortableValue

    def __init__(self, name: str, data: PortableValue): ...

def ws_task(
    listen_on: str,
    serve_on: str,
    static_dir: str,
    tick_speed: int,
    tick_hook: Callable[[bool, Literal[""] | RawRequest], None],
    time_book: Callable[[RawRequest], None],
): ...

class RawRequest:
    """A raw request information. This is an internal engine type,
    so you should not use it in the game logic.
    ---
    Available on: ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    handle: IOHandle
    sender: str
    content: Packet

class IOHandle:
    addr: str

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
    def on_update(self, show: Any) -> Status: ...
    async def on_request(
        self,
        show: Any,
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
    handle: IOHandle

    def __init__(self, identifier: str, name: str, score: int) -> None: ...
    def add_score(self, additional_score: int) -> int: ...
    def pack(self) -> str: ...
    @staticmethod
    def from_json(data: str) -> Player: ...

class Question:
    prompt: str
    media: MediaContent | None
    key: str
    score: int
    time: int
    choices: list[str] | None
    score_false: int | None
    explaination: str | None

    def __init__(
        self,
        prompt: str,
        key: str,
        score: int,
        time: int,
        choices: list[str],
        score_false: int,
        explaination: str,
        media: MediaContent | None = None,
    ): ...
    def pack(self) -> str: ...
    @staticmethod
    def from_json(data: str) -> Question: ...

class MediaContent:
    media_type: Literal["audio"] | Literal["image"] | Literal["video"]
    uri: str

    def __init__(
        self,
        media_type: Literal["audio"] | Literal["image"] | Literal["video"],
        uri: str,
    ) -> None: ...
    def pack(self) -> str: ...

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
            "choices": ["One", "Two", "Three", "69"],
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

    def pack(self) -> str: ...
    @staticmethod
    def from_json(data: str) -> QuestionBank: ...

class Timer:
    start_time: datetime.datetime
    paused_time: datetime.datetime
    paused_duration: datetime.timedelta
    is_paused: bool

    def __init__(self):
        """Creates a new timer, which pauses immidiately after creation."""

    def pause(self) -> None:
        """Pauses the timer."""

    def resume(self) -> None:
        """Resumes the timer."""

    def time_elapsed(self) -> datetime.timedelta:
        """Gets the time elapsed from the calling of `start()`,
        minus the pauses."""

    def pack(self) -> str: ...
    @staticmethod
    def from_json(target: str) -> Timer: ...

class Ticker:
    last_tick: datetime.datetime

    def tick(self, tick_speed: int):
        """Ensures the tick speed is met."""

class Credentials:
    username: str
    access_key: str

class AuthenticationStatus:
    success: bool
    message: str
    token: str

    def __init__(self, success: bool, message: str, token: str): ...

# = Union[
#     Query.Player,
#     Query.Question,
#     Query.QuestionBank,
#     Query.Show,
#     Query.Ticker,
#     Query.Timer,
#     Query.CurrentPart,
# ]

class Query(ABC):
    class Player(Query):
        index: str
        def __init__(self, index: str): ...

    class Question(Query):
        index: int
        def __init__(self, index: int): ...

    class PartByID(Query):
        index: int
        def __init__(self, index: int): ...

    class PartByName(Query):
        index: str
        def __init__(self, index: str): ...

    class State(Query):
        index: str
        def __init__(self, index: str): ...

    class PlayerList(Query):
        index: str
        def __init__(self): ...

    class QuestionBank(Query):
        pass

    class Ticker(Query):
        pass

    class Timer(Query):
        pass

    class CurrentPart(Query):
        pass

    class AvailableProcedures(Query):
        pass

    class StateList(Query):
        pass

    class PartList(Query):
        pass

    class Log(Query):
        index: int
        def __init__(self): ...

AvailableSound = (
    Literal["op-introduction"]
    | Literal["op-introducecontestants"]
    | Literal["common-startsection"]
    | Literal["common-dotdotdot"]
    | Literal["common-scoresum"]
    | Literal["tongket-4th"]
    | Literal["tongket-3rd"]
    | Literal["tongket-2nd"]
    | Literal["tongket-1st"]
    | Literal["tongket-award"]
    | Literal["khoidong-start"]
    | Literal["khoidong-ready"]
    | Literal["khoidong-3secs"]
    | Literal["khoidong-bgm"]
    | Literal["khoidong-correct"]
    | Literal["khoidong-incorrect"]
    | Literal["khoidong-bell"]
    | Literal["khoidong-complete"]
    | Literal["vcnv-start"]
    | Literal["vcnv-questionbox"]
    | Literal["vcnv-selectrow"]
    | Literal["vcnv-showquestion"]
    | Literal["vcnv-15secs"]
    | Literal["vcnv-showanswers"]
    | Literal["vcnv-correct"]
    | Literal["vcnv-incorrect"]
    | Literal["vcnv-bell"]
    | Literal["vcnv-bellcorrect"]
    | Literal["tangtoc-start"]
    | Literal["tangtoc-revealquestion"]
    | Literal["tangtoc-10secs"]
    | Literal["tangtoc-20secs"]
    | Literal["tangtoc-30secs"]
    | Literal["tangtoc-40secs"]
    | Literal["tangtoc-showanswers"]
    | Literal["tangtoc-correct"]
    | Literal["tangtoc-wrong"]
    | Literal["vedich-start"]
    | Literal["vedich-onstage"]
    | Literal["vedich-packagechoice"]
    | Literal["vedich-confirmchoice"]
    | Literal["vedich-15secs"]
    | Literal["vedich-20secs"]
    | Literal["vedich-poll"]
    | Literal["vedich-bell"]
    | Literal["vedich-correct"]
    | Literal["vedich-complete"]
)

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
def set_log_level(min_level: Level): ...
def log_debug(content: str): ...
def log_success(content: str): ...
def log_info(content: str): ...
def log_warning(content: str): ...
def log_error(content: str): ...

class LogEntry:
    timestamp: int
    level: int
    logger: str
    content: str
