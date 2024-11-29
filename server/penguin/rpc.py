import collections.abc
from os import initgroups
import traceback
import engine
import typing
import json

from config import config
from ._result import Result, Ok, Err
from ._option import Some, Null, Option
from .show import *
from .store import Writable


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


JSONPortable = collections.abc.Collection | int | float | str | collections.abc.Mapping


def portable_type(
    inp: typing.Any, serializer: typing.Callable | None = None
) -> engine.PortableType:
    if isinstance(inp, list):
        return engine.PortableType.ARRAY
    elif inp is None:
        return engine.PortableType.NULL
    elif isinstance(inp, int) or isinstance(inp, float):
        return engine.PortableType.NUMBER
    elif isinstance(inp, str):
        return engine.PortableType.STRING
    elif isinstance(inp, dict) or isinstance(inp, map):
        return engine.PortableType.OBJECT
    elif isinstance(inp, engine.PortableValue):
        return inp.data_type
    elif isinstance(inp, JSONPortable):
        return portable_type(inp)
    elif serializer is not None:
        return serializer(inp).data_type
    else:
        raise ValueError(
            f"{inp} of type {type(inp)} is not PortableValue or automatically derivable types, but serializer is None"
        )


def pack_portable_value(
    name: str,
    inp: typing.Any,
    serializer: typing.Callable[[typing.Any], engine.PortableValue] | None,
) -> engine.GameState:
    if isinstance(inp, engine.PortableValue):
        return engine.GameState(
            name=name,
            data=inp,
        )

    porttype: engine.PortableType
    if serializer is not None:
        return engine.GameState(name=name, data=serializer(inp))
    elif isinstance(inp, list):
        porttype = engine.PortableType.ARRAY
    elif inp is None:
        porttype = engine.PortableType.NULL
    elif isinstance(inp, int) or isinstance(inp, float):
        porttype = engine.PortableType.NUMBER
    elif isinstance(inp, str):
        porttype = engine.PortableType.STRING
    elif isinstance(inp, dict) or isinstance(inp, map):
        porttype = engine.PortableType.OBJECT
    elif isinstance(inp, JSONPortable):
        porttype = portable_type(inp)
    else:
        raise ValueError(
            f"{inp} of type {type(inp)} is not PortableValue or automatically derivable types, but serializer is None"
        )

    return engine.GameState(
        name=name,
        data=engine.PortableValue(
            json=json.dumps(inp, ensure_ascii=False), data_type=porttype
        ),
    )


ProcedureHandler = typing.Callable[
    # TODO - make the last argument the session ID
    [Show, engine.Packet.CallProcedure, engine.IOHandle, str],
    None,
]

T = typing.TypeVar(
    "T",
    collections.abc.Collection,
    int,
    float,
    str,
    collections.abc.Mapping,
    typing.Any,
)
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
        return isinstance(v, collections.abc.Iterable) and not isinstance(v, str)

    @staticmethod
    def bool(v: typing.Any):
        return isinstance(v, bool)


@typing.final
class RPCManager:
    """Listens to & manages Remote Procedure Calls and updating GameState"""

    def __init__(self, prefix: str = "engine") -> None:
        self.prefix: str = prefix
        self.procedures: list[engine.ProcedureSignature] = []
        self.proc_map: dict[
            str,
            ProcedureHandler,
        ] = {}
        # self.timer = engine.Timer()
        self.states: dict[str, engine.GameState] = {
            # "timer_json": engine.GameState(
            #     "timer_json",
            #     engine.PortableValue(self.timer.pack(), engine.PortableType.OBJECT),
            # )
        }
        self.states_writable: dict[str, Writable[typing.Any]] = {}
        self.orgtype_map: dict[str, type] = {
            # "timer_json": engine.Timer,
        }
        self.deser_map: dict[
            str, typing.Callable[[engine.PortableValue], typing.Any]
        ] = {}
        # self.add_procedure(
        #     self.timer_operation,
        #     signature=[("operation", engine.PortableType.STRING)],
        #     name="timer_operation",
        # )

    @typing.overload
    def get_state(self, name: str) -> T: ...
    @typing.overload
    def get_state(self, name: str, *, deser: typing.Callable[[str], T]) -> T: ...
    @typing.overload
    def get_state(self, name: str, *, raw: bool) -> str: ...
    @typing.overload
    def get_state(self, name: str, *, ret_raw: bool) -> engine.PortableValue: ...

    def get_state(
        self,
        name: str,
        *,
        deser: typing.Callable[[str], T] | None = None,
        raw: bool = False,
        ret_raw: bool = False,
    ) -> T | str | engine.PortableValue:
        # TODO - maintain cache for this. low priority.
        if deser is None and raw:
            raise ValueError("Both deser and raw cannot be none at the same time.")
        if deser:
            return deser(self.states[name].data.json)
        if raw:
            return self.states[name].data.json
        if ret_raw:
            return self.states[name].data
        return json.loads(self.states[name].data.json)

    def set_state(self, name: str, pvalue: engine.PortableValue):
        """Non type-checked and accepts raw PortableValue."""
        self.states[name] = engine.GameState(
            name=name,
            data=pvalue,
        )
        # engine.log_debug(f"(Logic) Broadcasting {name} = JSON(' {pvalue.json} ')")
        # original_type = self.orgtype_map[name]
        # if original_type is engine.Timer:
        #     pass
        # else:
        #     self.states_writable[name].set(self.deser_map[name](pvalue))

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
    ) -> Writable[engine.PortableValue]:
        """Creates a syncronized state handling raw `engine.Portable` values."""

    @typing.overload
    def use_state(
        self,
        name: str,
        initial_value: T,
        *,
        serializer: typing.Callable[[T], engine.PortableValue],
        deserializer: typing.Callable[[engine.PortableValue], T],
        hidden=False,
    ) -> Writable[T]:
        """Creates a syncronized state handling custom values with the provided
        serialize and deserializer."""

    @typing.overload
    def use_state(self, name: str, initial_value: T, *, hidden=False) -> Writable[T]:
        """Creates a syncronized state handling native JSON types with serialize and
        deserialization automatically inferred."""

    def use_state(
        self,
        name: str,
        initial_value: engine.PortableValue | T,
        *,
        serializer: typing.Callable[[T], engine.PortableValue] | None = None,
        deserializer: typing.Callable[[engine.PortableValue], T] | None = None,
        hidden=False,
    ) -> Writable[engine.PortableValue] | Writable[T]:
        output = Writable(initial_value)
        initial_gamestate = pack_portable_value(name, output.get(), serializer)
        data_type = initial_gamestate.data.data_type
        self.states[name] = initial_gamestate
        self.orgtype_map[name] = type(initial_value)
        self.states_writable[name] = output
        if deserializer and serializer:
            self.deser_map[name] = deserializer
            output.subscribe(
                lambda value: self.set_state(name, serializer(value))  # type: ignore[reportArgumentType]
            )
        elif isinstance(initial_value, engine.PortableValue):
            self.deser_map[name] = lambda x: x

            def type_is_correct(
                value: engine.PortableValue, ptype: engine.PortableType
            ) -> bool:
                return ptype == value.data_type

            def error(value, ptype):
                raise TypeError(
                    f"Type mismatch: expected '{ptype}', found '{portable_type(value)}'"
                )

            output.subscribe(lambda value: self.set_state(name, value) if config().checkRPCTypes and type_is_correct(value, data_type) else error(value, data_type))  # type: ignore[reportArgumentType]
        else:
            self.deser_map[name] = lambda x: json.loads(x.json)
            output.subscribe(
                lambda value: self.set_state(
                    name,
                    engine.PortableValue(
                        json=json.dumps(value, ensure_ascii=False), data_type=data_type
                    ),
                )
            )

        return output  # type: ignore[reportReturnType]

    def add_procedure(
        self,
        proc: ProcedureHandler,
        *,
        signature: Signature,
        hidden: bool = False,
        name: str | None = None,
    ) -> "RPCManager":
        n = name if name else proc.__name__
        # if n == "timer_operation":
        #     proc_ident = "engine::" + n
        # else:
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
                        self.add_procedure(p1, hidden=p2, signature=signature)  # type: ignore[reportArgumentType]
                    if Is.str(p1) and Is.proc(p2):
                        self.add_procedure(p2, name=p1, signature=signature)  # type: ignore[reportArgumentType]
                case (p1, signature):
                    self.add_procedure(p1, signature=signature)
                case _:  # type: ignore[reportArgumentType]
                    raise ValueError(f"Unknown procedure prototype: {t}")  # type: ignore[reportArgumentType]

        return self

    async def handle(
        self,
        show: Show,
        packet: engine.Packet,
        handle: engine.IOHandle,
        addr: str,
    ) -> Result[bool, str]:
        match packet:
            case engine.Packet.CallProcedure():
                call = packet.data
                for proc in self.procedures:
                    if proc.name == call.name:
                        engine.log_debug(f"Calling procedure {call.name}")
                        # TODO - type checking for procedure arguments.
                        try:
                            engine.log_debug(
                                f"Executed {proc.name} → {self.proc_map[proc.name](show, packet, handle, addr)}"
                            )
                        except Exception as e:
                            engine.log_error(traceback.format_exc())

                        return Ok(True)
                else:
                    if call.name.startswith(self.prefix):
                        engine.log_warning(
                            f"Cannot find procedure with name `{call.name}` in {[p.name for p in self.procedures]}. Call ignored."
                        )
                    return Ok(False)
            case engine.Packet.Query():
                request = packet.data
                match request:
                    case engine.Query.AvailableProcedures():
                        await handle.send(
                            engine.Packet.ProcedureList(self.procedures).pack()
                        )
                        return Ok(True)
                    case engine.Query.StateList():
                        await handle.send(
                            engine.Packet.StateList(list(self.states.values())).pack()
                        )
                        engine.log_warning(f"{self.prefix} sent statelist")
                        return Ok(True)
                    case engine.Query.Timer():
                        await handle.send(engine.Packet.Timer(show.timer.get()).pack())
                    case _:
                        return Ok(False)

            case engine.Packet.UpdateState():
                update = packet.data
                # if update.name == "timer_json":
                #     engine.log_debug(f"Setting timer to {update.data.json}")
                #     self.timer = engine.Timer.from_json(update.data.json)
                # TODO - type checking for gamestate updates
                engine.log_debug(
                    f"Changing game state: {update.name} = {update.data.json!r}"
                )
                try:
                    # engine.log_debug(
                    #     f"(WSUpdated) Broadcasting {update.name} = JSON(' {json.dumps(update.data.json, ensure_ascii=False)} ')"
                    # )
                    self.states[update.name] = update
                    self.states_writable[update.name].set(
                        self.deser_map[update.name](update.data)
                    )
                    await show.session_manager.broadcast(
                        engine.Packet.State(self.states[update.name]).pack()
                    )
                    return Ok(True)
                except KeyError:
                    if update.name.startswith(self.prefix):
                        engine.log_warning(
                            f"Cannot find procedure with name `{update.name}`. Call ignored."
                        )
                    return Ok(False)
            case _:
                return Ok(False)
        return Ok(False)
