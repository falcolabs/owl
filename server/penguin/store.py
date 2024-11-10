import typing

T = typing.TypeVar("T")


class Readable(typing.Generic[T]):
    def __init__(self, initial_value: T) -> None:
        self._subscribers: list[typing.Callable[[T], None]] = []
        self._value: T = initial_value

    @property
    def inner(self) -> T:
        return self.get()

    def subscribe(
        self, callback: typing.Callable[[T], None]
    ) -> typing.Callable[[], None]:
        """Subscribes to a value.
        :param callback: the function to invoke when the value updates.
        :returns: a hook to remove the listener.
        """
        self._subscribers.append(callback)
        callback(self._value)
        remove_at = len(self._subscribers) - 1

        def remove():
            del self._subscribers[remove_at]

        return remove

    def get(self) -> T:
        """Returns the current value."""
        return self._value

    @typing.override
    def __eq__(self, value: object, /) -> bool:
        raise SyntaxError(
            "Stores cannot be compared. Try comparing its value, `.inner`,`.get()`, or subscribing to its value."
        )

    @typing.override
    def __str__(self) -> str:
        raise SyntaxError(
            "Stores cannot be stringified. Try stringifing its value, `.inner`,`.get()`, or subscribing to its value."
        )

    @typing.override
    def __repr__(self) -> str:
        raise SyntaxError(
            "Stores cannot be repr-ed. Try repr-ing its value, `.inner`,`.get()`, or subscribing to its value."
        )


class Writable(Readable[T]):
    @property
    @typing.override
    def inner(self) -> T:
        return self.get()

    @inner.setter
    def set_inner(self, value: T):
        return self.set(value)

    def set(self, new_value: T):
        """Changes the contained value and notify the listeners."""
        self._value: T = new_value
        for cb in self._subscribers:
            cb(self._value)
