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
        self.change_listen: dict[str, typing.Callable[[engine.PortableValue], None]] = (
            {}
        )

    @typing.overload
    def get_state(self, name: str) -> T: ...
    @typing.overload
    def get_state(self, name: str, *, deser: typing.Callable[[str], T]) -> T: ...
    @typing.overload
    def get_state(self, name: str, *, raw: bool = True) -> str: ...
    @typing.overload
    def get_state(self, name: str, *, ret_raw: bool = True) -> engine.PortableValue: ...

    def get_state(
        self,
        name: str,
        *,
        deser: typing.Callable[[str], T] | None = None,
        raw: bool = False,
        ret_raw: bool = False,
    ) -> T | str | engine.PortableValue:
        # TODO - maintain cache for this. low priority.
        if deser is None and raw is None:
            raise ValueError("Both deser and raw cannot be none at the same time.")
        if deser:
            return deser(self.states[name].data.json)
        if raw:
            return self.states[name].data.json
        if ret_raw:
            return self.states[name].data
        return json.loads(self.states[name].data.json)  # type: ignore

    @typing.overload
    def set_state(
        self,
        name: str,
        value: T,
        *,
        ptype: engine.PortableType,
    ): ...
    @typing.overload
    def set_state(
        self,
        name: str,
        value: str,
        *,
        ser: typing.Callable[[T], str],
        ptype: engine.PortableType | None = None,
    ): ...
    @typing.overload
    def set_state(
        self,
        name: str,
        value: engine.PortableValue,
    ): ...

    def set_state(
        self,
        name: str,
        value: T | engine.PortableValue | str,
        *,
        ser: typing.Callable[[T], str] | None = None,
        ptype: engine.PortableType | None = None,
    ):
        def typecheck() -> bool:
            if isinstance(value, engine.PortableValue):
                return True
            if ser:
                return True
            return ptype != portable_type(value)

        if config().checkRPCTypes and typecheck():
            raise TypeError(
                f"Type mismatch: expected '{ptype}', found '{portable_type(value)}'"
            )

        if isinstance(value, engine.PortableValue):
            return self._set_state_value(
                name=name,
                pvalue=value,
            )
        if ser is not None and ptype is not None:
            return self._set_state_value(
                name=name,
                pvalue=engine.PortableValue(json=ser(value), data_type=ptype),  # type: ignore
            )

        if not ptype:
            raise ValueError("ptype must be provided.")

        return self._set_state_value(
            name=name,
            pvalue=engine.PortableValue(json=json.dumps(value), data_type=ptype),
        )

    def _set_state_value(self, name: str, pvalue: engine.PortableValue):
        """Non type-checked and accepts raw PortableValue."""
        self.states[name] = engine.GameState(
            name=name,
            data=pvalue,
        )
        engine.log_debug(
            f"Broadcasting gamestate change & calling hooks: Logic: {name} = {pvalue.json}"
        )
        if name in self.change_listen:
            self.change_listen[name](pvalue)
        TASK_POOL.append(
            LOOP.create_task(
                SESSION_MAN.broadcast(engine.Packet.State(self.states[name]).pack())
            )
        )

    @typing.overload
    def use_state(
        self,
        name: str,
        initial_value: engine.PortableValue,
        *,
        hidden=False,
    ) -> tuple[typing.Callable[[], str], typing.Callable[[str], None]]: ...

    @typing.overload
    def use_state(
        self,
        name: str,
        initial_value: str,
        *,
        serializer: typing.Callable[[T], str],
        deserializer: typing.Callable[[str], T],
        hidden=False,
    ) -> tuple[typing.Callable[[], T], typing.Callable[[T], None]]: ...

    @typing.overload
    def use_state(
        self, name: str, initial_value: T, *, hidden=False
    ) -> tuple[typing.Callable[[], T], typing.Callable[[T], None]]: ...

    def use_state(
        self,
        name: str,
        initial_value: T | str | engine.PortableValue,
        *,
        serializer: typing.Callable[[T], str] | None = None,
        deserializer: typing.Callable[[str], T] | None = None,
        hidden=False,
    ) -> (
        tuple[typing.Callable[[], T], typing.Callable[[T], None]]
        | tuple[typing.Callable[[], str], typing.Callable[[str], None]]
        | tuple[
            typing.Callable[[], engine.PortableValue],
            typing.Callable[[engine.PortableValue], None],
        ]
    ):
        porttype = (
            initial_value.data_type
            if isinstance(initial_value, engine.PortableValue)
            else portable_type(initial_value)
        )
        if isinstance(initial_value, engine.PortableValue):
            if not isinstance(initial_value, str):
                raise ValueError("initial_value must be str if ptype is set.")
            self.states[name] = engine.GameState(
                name=name,
                data=initial_value,
            )
        elif serializer:
            self.states[name] = engine.GameState(
                name=name,
                data=engine.PortableValue(
                    json=serializer(initial_value), data_type=porttype  # type: ignore
                ),
            )
        else:
            self.states[name] = engine.GameState(
                name=name,
                data=engine.PortableValue(
                    json=json.dumps(initial_value), data_type=porttype
                ),
            )

        get, set = None, None

        if deserializer and serializer:

            def get_ser() -> T:
                return self.get_state(name, deser=deserializer)

            def set_ser(value: str):
                self.set_state(name, value, ser=serializer, ptype=porttype)

            get, set = get_ser, set_ser

        elif isinstance(initial_value, engine.PortableValue):

            def get_raw() -> engine.PortableValue:
                return self.get_state(name, ret_raw=True)

            def set_raw(value: engine.PortableValue):  # type: ignore
                self.set_state(name, value)

            get, set = get_raw, set_raw

        else:

            def get_nor() -> T:
                return self.get_state(name)

            def set_nor(value: T):
                self.set_state(name, value, ptype=porttype)

            get, set = get_nor, set_nor

        return get, set  # type: ignore

    def on_change(self, name: str, F: typing.Callable[[engine.PortableValue], None]):
        self.change_listen[name] = F

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

        self._set_state_value(
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
                        f"Broadcasting gamestate change & calling hooks: WSUpdated: {update.name} = {json.dumps(update.data.json)}"
                    )
                    if update.name in self.change_listen:
                        self.change_listen[update.name](update.data)
                    await SESSION_MAN.broadcast(
                        engine.Packet.State(self.states[update.name]).pack()
                    )
                except KeyError:
                    engine.log_warning(
                        f"Cannot find procedure with name `{update.name}`. Call ignored."
                    )
        return Ok()
