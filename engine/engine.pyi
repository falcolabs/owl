from typing import Any, Optional, Callable, Literal, Union, Iterable, Mapping
from abc import abstractmethod, ABC

PacketData = Union[
    AuthenticationStatus,
    PartProperties,
    Player,
    Credentials,
    Question,
    QuestionBank,
    Query,
    Show,
    Ticker,
    Timer,
    str,
    list[ProcedureSignature],
    ProcedureCall,
    GameStateUpdate,
    list[GameStatePrototype],
]
"""All the possible values in a packet's data."""

class Packet(ABC):
    """An algebraic datatype encapsulating data, serialize and
    deserializable to and from JSON. Only `serde@rust` may
    deserialize a `Packet`, while serializing is available
    everywhere using `.pack()` or `str()`.
    ---
    **Availability:** ✓ Python, ✓ Rust, ✗ JavaScript, ✓ WASM

    ---
    ### Usage
    A `match` statement may be used to differentiate between these
    variants:
    ```py
    match packet:
        case Packet.AuthStatus():
            ...
        case _:
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

    class Show(Packet):
        """A packet containing the entire show's details"""

        data: Show
        def __init__(self, data: Show): ...

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

    class GameState(Packet):
        """A packet containing the state of the game."""

        data: list[GameStatePrototype]
        def __init__(self, data: list[GameStatePrototype]): ...

    class UpdateGameState(Packet):
        """A packet updating the state of the game."""

        data: GameStateUpdate
        def __init__(self, data: GameStateUpdate): ...

    class Unknown(Packet):
        """An packet used to contain unknown data."""

        data: str
        def __init__(self, data: str): ...

    data: PacketData

    @abstractmethod
    def __init__(self, data: PacketData): ...
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
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM"""

    json: str
    data_type: PortableType

    def __init__(self, data: str, type: PortableType): ...
    def as_str(self) -> str: ...
    def as_int(self) -> int: ...
    def as_float(self) -> float: ...

class ProcedureSignature:
    """The signature for a procedure.

    ---
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    name: str
    hidden: bool

    def __init__(
        self, name: str, hidden: bool, args: list[tuple[str, PortableType]]
    ): ...

class ProcedureCall:
    """A procedure call.

    ---
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    name: str
    args: list[tuple[str, PortableValue]]

class GameStatePrototype:
    """A game state's type and value.

    ---
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM"""

    name: str
    hidden: bool

    def __init__(self, name: str, hidden: bool, data_type: PortableType): ...

class GameStateUpdate:
    """
    An update to the game state.

    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM"""

    name: str
    data: PortableValue

class Show:
    """An object containing all the resources available globally
    in the show. This object should be a global variable, or otherwise
    publicly and statically accessible.
    ---
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

    name: str
    """The name of the show."""
    parts: list[Part]
    """The parts included in the show."""
    tick_speed: int
    """The show's tick speed."""
    current_part: int
    """The current part index."""
    players: list[Player]
    """The players present"""
    qbank: QuestionBank
    """All the questions the show contains"""
    ticker: Ticker
    """The show's ticker"""
    timer: Timer
    """The show's timer"""

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
        """Starts the show. This is a blocking function, and will only stop
        when the show is terminated by the user.

        :param: `listen_on` the host and port for the server to listen on. Resource will be hosted on `/`, WebSocket PI on `/harlem`
        :param: `serve_dir` where the static content will be hosted at. May contain unsolicited WebAssembly files.
        :param: `static_dir` where the static content lives. Should contain `404.html`.

        ## Usage
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
    """A raw request information. This is an internal engine type,
    so you should not use it in the game logic.
    ---
    **Availability:** ✓ Python, ✓ Rust, ✓ JavaScript, ✓ WASM
    """

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
    handle: IOHandle

    def __init__(self, identifier: str, name: str, score: int) -> None: ...
    def add_score(self, additional_score: int) -> int: ...

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

    class QuestionBank(Query):
        pass

    class Show(Query):
        pass

    class Ticker(Query):
        pass

    class Timer(Query):
        pass

    class CurrentPart(Query):
        pass

    class AvailableProcedures(Query):
        pass

    class GameState(Query):
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
def set_log_level(min_level: Level): ...
def log_debug(content: str): ...
def log_success(content: str): ...
def log_info(content: str): ...
def log_warning(content: str): ...
def log_error(content: str): ...
