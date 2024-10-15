"""Rust-like None handling primitive."""

import typing
import abc

T = typing.TypeVar("T")


class Option(typing.Generic[T]):
    """Rust-like None handling primitive."""

    _value: T | None
    __match_args__ = ("value",)

    def __init__(self, value: T | None):
        self._value = value

    @abc.abstractmethod
    def is_some(self) -> bool:
        pass

    def unwrap(self) -> T:
        """Raises an exeption if the value contained inside is of the Null variant."""
        if not self.is_some():
            raise Exception(f"Option.unwrap() on a Null value: {self._value}")
        return self._value  # type: ignore[reportReturnType]

    def expect(self, msg: str) -> T:
        """Raises an exeption with the provided message if the value contained
        inside is of the Null variant."""
        if not self.is_some():
            raise Exception(msg)
        return self._value  # type: ignore[reportReturnType]

    def unwrap_or(self, f: typing.Callable[[], T]) -> T:
        """Calls the given callback if the value
        contained inside is of the Null variant."""
        if not self.is_some():
            return f(self._value)  # type: ignore[reportReturnType]
        return self._value  # type: ignore[reportReturnType]


class Some(Option[T]):

    def __init__(self, value: T):
        if value is None:
            raise ValueError("Some cannot be None")
        self._value = value

    @typing.override
    def is_some(self):
        return True


class Null(Option[T]):
    def __init__(self):
        self._value = None

    @typing.override
    def is_some(self):
        return False
