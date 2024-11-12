"""Rust-like None handling primitive."""

from dataclasses import dataclass
import typing
import abc

T = typing.TypeVar("T")


class _OptionLogic:
    """Rust-like None handling primitive."""

    value: typing.Any

    def __init__(self, value: typing.Any):
        self.value = value

    @abc.abstractmethod
    def is_some(self) -> bool:
        pass

    def unwrap(self) -> typing.Any:
        """Raises an exeption if the value contained inside is of the Null variant."""
        if not self.is_some():
            raise Exception(f"Option.unwrap() on a Null value: {self.value}")
        return self.value

    def expect(self, msg: str) -> typing.Any:
        """Raises an exeption with the provided message if the value contained
        inside is of the Null variant."""
        if not self.is_some():
            raise Exception(msg)
        return self.value

    def unwrap_or(self, f: typing.Callable[[], T]) -> T:
        """Calls the given callback if the value
        contained inside is of the Null variant."""
        if not self.is_some():
            return f(self.value)  # type: ignore[reportReturnType]
        return self.value


@typing.final
@dataclass
class Some(_OptionLogic, typing.Generic[T]):
    value: T

    def __init__(self, value: T):
        if value is None:
            raise ValueError("Some cannot be None")
        self.value = value

    @typing.override
    def is_some(self):
        return True

    @typing.override
    def unwrap(self) -> T:
        return super().unwrap()

    @typing.override
    def expect(self, msg: str) -> T:
        return super().expect(msg)


@typing.final
@dataclass
class Null(_OptionLogic):
    def __init__(self):
        self.value = None

    @typing.override
    def is_some(self):
        return False

    @typing.override
    def unwrap(self):
        super().unwrap()

    @typing.override
    def expect(self, msg: str):
        super().expect(msg)


type Option[T] = Some[T] | Null
