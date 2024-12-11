"""Manages configuration entries.
"""

from __future__ import annotations

import json
import typing
import engine
import collections.abc
from typing import Any, TypedDict, override


class ConfigurationValue:
    def __init__(self, hive, _convert: bool = True) -> None:
        if not _convert:
            self._hive: Any = hive
        else:
            self._hive = self.rec_convert(hive)

    def rec_convert(
        self, inp: dict | list | str | int | float | bool
    ) -> (
        dict[typing.Any, ConfigurationValue]
        | list[ConfigurationValue]
        | str
        | int
        | float
        | bool
    ):
        res = None
        if isinstance(inp, collections.abc.Mapping):
            r = {}
            for k, v in inp.items():
                r[k] = self.rec_convert(v)
            res = ConfigurationValue(r, False)
        elif isinstance(inp, str):
            res = inp
        elif isinstance(inp, collections.abc.Iterable):
            r = []
            for v in inp:
                r.append(self.rec_convert(v))
            res = ConfigurationValue(r, False)
        else:
            res = inp

        return res  # type: ignore[reportReturnType]

    def __getattr__(self, name: str) -> typing.Any:
        try:
            if isinstance(self._hive, ConfigurationValue):
                if isinstance(self._hive._hive, collections.abc.Mapping):
                    return self._hive._hive[name]
            if isinstance(self._hive, collections.abc.Mapping):
                return self._hive[name]
        except KeyError:
            pass
        raise KeyError(
            f"Cannot find key '{name}' in available config entry: {self._hive.keys() if isinstance(self._hive, collections.abc.Mapping) else self._hive}"
        )

    def __getitem__(self, index: slice) -> typing.Any:
        if isinstance(self._hive, ConfigurationValue):
            if isinstance(
                self._hive._hive, collections.abc.Sequence
            ) and not isinstance(self._hive._hive, str):
                return self._hive._hive[index]
        if isinstance(self._hive, collections.abc.Sequence) and not isinstance(
            self._hive, str
        ):
            return self._hive[index]
        raise KeyError(f"Cannot find index '{index}' in {self}")

    @override
    def __eq__(self, other):
        if isinstance(other, ConfigurationValue):
            return self._hive == other._hive
        return self._hive == other

    @override
    def __str__(self) -> str:
        return str(self._hive)

    @override
    def __repr__(self) -> str:
        return f"ConfigurationValue({self._hive})"


class UserCredentials(ConfigurationValue):
    fullName: str
    username: str
    accessKey: str


class ConfigHive(ConfigurationValue):
    listenOn: Any
    serveDir: str
    staticDir: str
    checkRPCTypes: bool
    debug: bool
    tickSpeed: int
    credentials: list[UserCredentials]
    game: Any
    gameAssets: list[str]


CFG_HIVE: ConfigHive


def load(fp: str):
    global CFG_HIVE
    with open(fp, "r", encoding="utf8") as f:
        CFG_HIVE = ConfigHive(json.load(f))


def config() -> ConfigHive:
    return CFG_HIVE
