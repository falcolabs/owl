"""Rust-like Error handling primitive."""

import typing
import abc
import sys
import traceback
import engine

T = typing.TypeVar("T")
E = typing.TypeVar("E")


def handle_exception(
    got_exception_type: type[Exception],
    got_exception: Exception,
    got_traceback,
):
    listing = traceback.format_exception(
        got_exception_type, got_exception, got_traceback
    )
    filelist = [
        "org.python.pydev",
        "server/penguin/_option.py",
        "server/penguin/_error.py",
    ]  # Remove debugger and error handling modules.
    listing = [item for item in listing if len([f for f in filelist if f in item]) == 0]
    files = [line for line in listing if line.startswith("  File")]
    if len(files) == 1:
        # only one file, remove the header.
        del listing[0]
    engine.log_error(
        "Exception raised without being caught. Exiting." + "\n" + "".join(listing)
    )


def set_error_hook():
    sys.excepthook = handle_exception


class _ResultLogic(abc.ABC):
    """Rust-like Error handling primitive."""

    value: typing.Any

    def __init__(self, value: typing.Any) -> None:
        self.value = value

    @abc.abstractmethod
    def is_ok(self) -> bool:
        pass

    def unwrap(self) -> typing.Any:
        """Raises an exeption if the value contained inside is of the Err variant."""
        if not self.is_ok():
            raise Exception(f"Result.unwrap() on an Err value: Err({self.value})")
        return self.value

    def expect(self, msg: str) -> typing.Any:
        """Raises an exeption with the provided message if the value contained
        inside is of the Err variant."""
        if not self.is_ok():
            raise Exception(msg)
        return self.value

    def unwrap_or(self, f: typing.Callable[[E], T]) -> T:
        """Calls the given callback if the value
        contained inside is of the Err variant."""
        if not self.is_ok():
            return f(self.value)
        return self.value


@typing.final
class Ok(_ResultLogic, typing.Generic[T]):
    value: T

    @typing.override
    def unwrap(self) -> T:
        return super().unwrap()

    @typing.override
    def expect(self, msg: str) -> T:
        return super().expect(msg)

    def __init__(self, value: T = None) -> None:
        self.value = value

    @typing.override
    def is_ok(self):
        return True


@typing.final
class Err(_ResultLogic, typing.Generic[E]):
    value: E

    def __init__(self, value=None) -> None:
        self.value = value

    @typing.override
    def is_ok(self):
        return False

    @typing.override
    def unwrap(self):
        super().unwrap()

    @typing.override
    def expect(self, msg: str):
        super().expect(msg)


type Result[T, E] = Ok[T] | Err[E]
