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


class Result(typing.Generic[T, E]):
    """Rust-like Error handling primitive."""

    _value: T | E
    __match_args__ = ("value",)

    def __init__(self, value: T | E) -> None:
        self._value = value

    @abc.abstractmethod
    def is_ok(self) -> bool:
        pass

    def unwrap(self) -> T:
        """Raises an exeption if the value contained inside is of the Err variant."""
        if not self.is_ok():
            raise Exception(f"Result.unwrap() on an Err value: Err({self._value})")
        return self._value  # type: ignore

    def expect(self, msg: str) -> T:
        """Raises an exeption with the provided message if the value contained
        inside is of the Err variant."""
        if not self.is_ok():
            raise Exception(msg)
        return self._value  # type: ignore

    def unwrap_or(self, f: typing.Callable[[E], T]) -> T:
        """Calls the given callback if the value
        contained inside is of the Err variant."""
        if not self.is_ok():
            return f(self._value)  # type: ignore
        return self._value  # type: ignore


class Ok(Result[T, E]):

    def __init__(self, value: T = None) -> None:
        self._value = value

    @typing.override
    def is_ok(self):
        return True


class Err(Result[T, E]):

    def __init__(self, value=None) -> None:
        self._value = value

    @typing.override
    def is_ok(self):
        return False
