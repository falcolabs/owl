import json
import typing
import engine
from typing import TypedDict


class ConfigurationValue:
    def __init__(self, hive) -> None:
        self._hive = self.rec_convert(hive)

    def rec_convert(
        self, inp: dict | list | str | int | float | bool
    ) -> (
        "ConfigurationValue"
        | "list[ConfigurationValue | str | int | float | bool]"
        | str
        | int
        | float
        | bool
    ):
        res = None
        if isinstance(inp, typing.Mapping):
            r = {}
            for k, v in inp.items():
                r[k] = self.rec_convert(v)
            res = r
        elif isinstance(inp, typing.Iterable):
            r = []
            for v in inp:
                r.append(self.rec_convert(v))
            res = r
        else:
            res = inp

        return res  # type: ignore

    def __getattribute__(self, name: str) -> typing.Any:
        return self._hive.__getattribute__(name)


class UserCredentials(ConfigurationValue):
    fullName: str
    username: str
    accessKey: str


class ConfigHive(ConfigurationValue):
    listenOn: str
    serveDir: str
    staticDir: str
    credentials: list[UserCredentials]


CONFIG: ConfigHive


def load(fp: str):
    global CFG_HIVE
    with open(fp, "w", encoding="utf8") as f:
        CFG_HIVE = ConfigHive(json.load(f))


def config() -> ConfigHive:
    return CONFIG
