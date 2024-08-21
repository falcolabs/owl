import engine
import typing
import json

from config import config
from ._result import Result, Ok, Err
from ._option import Some, Null, Option
from .show import LOOP, SESSION_MAN, TASK_POOL


def str_portable_type(inp: str) -> engine.PortableType:
    if inp.startswith("list"):
        return engine.PortableType.ARRAY
    if inp.startswith("None"):
        return engine.PortableType.NULL
    if inp.startswith("int") or inp.startswith("float"):
        return engine.PortableType.NUMBER
    if inp.startswith("str"):
        return engine.PortableType.STRING
    if inp.startswith("dict") or inp.startswith("map"):
        return engine.PortableType.OBJECT
    else:
        raise TypeError(f"Unsupported argument type: `{inp}`")


def portable_type(inp: object) -> engine.PortableType:
    if isinstance(inp, list):
        return engine.PortableType.ARRAY
    if inp is None:
        return engine.PortableType.NULL
    if isinstance(inp, int) or isinstance(inp, float):
        return engine.PortableType.NUMBER
    if isinstance(inp, str):
        return engine.PortableType.STRING
    if isinstance(inp, dict) or isinstance(inp, map):
        return engine.PortableType.OBJECT
    else:
        raise TypeError(f"Unsupported argument type: `{inp}`")


ProcedureHandler = typing.Callable[
    [engine.Show, engine.Packet.CallProcedure, engine.IOHandle, str],
    None,
]

T = typing.TypeVar("T", list, int, float, str, dict)
Signature = list[tuple[str, engine.PortableType]]


class Is:
    """Basic typechecking class"""

    @staticmethod
    def proc(v: typing.Any):
        return isinstance(v, typing.Callable)

    @staticmethod
    def str(v: typing.Any):
        return isinstance(v, str)

    @staticmethod
    def signature(v: typing.Any):
        return isinstance(v, typing.Iterable) and not isinstance(v, str)

    @staticmethod
    def bool(v: typing.Any):
        return isinstance(v, bool)


class RPCManager:
    """Listens to & manages Remote Procedure Calls and updating GameState"""

    def __init__(self, prefix: str = "") -> None:
        self.prefix = prefix
        self.procedures: list[engine.ProcedureSignature] = []
        self.proc_map: dict[
            str,
            ProcedureHandler,
        ] = {}
        self.timer = engine.Timer()
        self.states: dict[str, engine.GameState] = {
            "timer_json": engine.GameState(
                "timer_json",
                engine.PortableValue(self.timer.pack(), engine.PortableType.OBJECT),
            )
        }
        self.add_procedure(
            self.timer_operation,
            signature=[("operation", engine.PortableType.STRING)],
            name="timer_operation",
        )

    def get_state(self, name: str) -> T:
        # TODO - maintain cache for this
        return json.loads(self.states[name].data.json)  # type: ignore

    def set_state(self, name: str, ptype: engine.PortableType, value: T):
        if config().checkRPCTypes and ptype != portable_type(value):
            raise TypeError(
                f"Type mismatch: expected '{ptype}', found '{portable_type(value)}'"
            )
        self.set_state_force(
            name=name,
            pvalue=engine.PortableValue(json=json.dumps(value), data_type=ptype),
        )

    def set_state_force(self, name: str, pvalue: engine.PortableValue):
        """Non type-checked and accepts raw PortableValue."""
        self.states[name] = engine.GameState(
            name=name,
            data=pvalue,
        )
        engine.log_debug(
            f"Broadcasting gamestate change: Logic: {name} = {pvalue.json}"
        )
        TASK_POOL.append(
            LOOP.create_task(
                SESSION_MAN.broadcast(engine.Packet.State(self.states[name]).pack())
            )
        )

    def use_state(
        self, name: str, initial_value: T, hidden=False
    ) -> tuple[typing.Callable[[], T], typing.Callable[[T], None]]:
        ptype = portable_type(initial_value)
        self.states[name] = engine.GameState(
            name=name,
            data=engine.PortableValue(json=json.dumps(initial_value), data_type=ptype),
        )
        # self.state_map[name] = initial_value

        def get() -> T:
            return self.get_state(name)

        def set(value: T):
            self.set_state(name, ptype, value)

        return get, set

    def add_procedure(
        self,
        proc: ProcedureHandler,
        *,
        signature: Signature,
        hidden: bool = False,
        name: str | None = None,
    ) -> "RPCManager":
        n = name if name else proc.__name__
        if n == "timer_operation":
            proc_ident = "engine::" + n
        else:
            proc_ident = self.prefix + "::" + n

        self.procedures.append(
            engine.ProcedureSignature(
                name=proc_ident,
                hidden=hidden,
                args=signature,
            )
        )
        self.proc_map[proc_ident] = proc

        return self

    def add_procedures(
        self,
        proc_list: list[
            tuple[ProcedureHandler, bool, Signature]
            | tuple[str, ProcedureHandler, bool, Signature]
            | tuple[str, ProcedureHandler, Signature]
            | tuple[ProcedureHandler, Signature]
        ],
    ) -> "RPCManager":
        for t in proc_list:
            match t:
                case (p1, p2, p3, signature):
                    self.add_procedure(p2, name=p1, hidden=p3, signature=signature)
                case (p1, p2, signature):
                    if Is.proc(p1) and Is.bool(p2):
                        self.add_procedure(p1, hidden=p2, signature=signature)  # type: ignore
                    if Is.str(p1) and Is.proc(p2):
                        self.add_procedure(p2, name=p1, signature=signature)  # type: ignore
                case (p1, signature):
                    self.add_procedure(p1, signature=signature)
                case _:
                    raise ValueError(f"Unknown procedure prototype: {t}")

        return self

    def timer_operation(
        self,
        _: engine.Show,
        callproc: engine.Packet.CallProcedure,
        _2: engine.IOHandle,
        _3,
    ):
        operation: typing.Literal["start", "pause", "reset"] = json.loads(
            callproc.data.args[0][1].json
        )
        engine.log_debug(f"Processing timer operation: {operation}")

        match operation:
            case "start":
                self.timer.resume()
            case "pause":
                self.timer.pause()
                engine.log_debug(f"paused time: {self.timer.time_elapsed()}")
            case "reset":
                self.timer = engine.Timer()
            case _:
                engine.log_warning(f"Timer operation not found: {operation}. Ignoring.")

        self.set_state_force(
            "timer_json",
            engine.PortableValue(
                json=self.timer.pack(), data_type=engine.PortableType.OBJECT
            ),
        )

    async def handle(
        self,
        show: engine.Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ) -> Result[None, str]:
        match packet:
            case engine.Packet.CallProcedure():
                call = packet.data
                for proc in self.procedures:
                    if proc.name == call.name:
                        engine.log_debug(f"Calling procedure {call.name}")
                        # TODO - type checking for procedure arguments.
                        return Ok(self.proc_map[proc.name](show, packet, handle, addr))
                else:
                    engine.log_warning(
                        f"Cannot find procedure with name `{call.name}` in {[p.name for p in self.procedures]}. Call ignored."
                    )
                    return Ok()
            case engine.Packet.Query():
                request = packet.data
                match request:
                    case engine.Query.AvailableProcedures():
                        await handle.send(
                            engine.Packet.ProcedureList(self.procedures).pack()
                        )
                    case engine.Query.StateList():
                        await handle.send(
                            engine.Packet.StateList(list(self.states.values())).pack()
                        )
                    case engine.Query.Timer():
                        await handle.send(engine.Packet.Timer(self.timer).pack())
            case engine.Packet.UpdateState():
                update = packet.data
                if update.name == "timer_json":
                    engine.log_debug(f"Setting timer to {update.data.json}")
                    self.timer = engine.Timer.from_json(update.data.json)
                # TODO - type checking for gamestate updates
                engine.log_debug(
                    f"Changing game state {update.name} to {update.data.json}"
                )
                try:
                    self.states[update.name] = update
                    engine.log_debug(
                        f"Broadcasting gamestate change: WSUpdated: {update.name} = {json.dumps(update.data.json)}"
                    )
                    await SESSION_MAN.broadcast(
                        engine.Packet.State(self.states[update.name]).pack()
                    )
                except KeyError:
                    engine.log_warning(
                        f"Cannot find procedure with name `{update.name}`. Call ignored."
                    )
        return Ok()
