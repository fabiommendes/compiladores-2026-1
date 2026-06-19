from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import Callable, Iterator, MutableMapping

from .ast import Function, LoxPrimitive
from . import interpreter

type LoxValue = LoxPrimitive | LoxCallable


class LoxError(Exception):
    def __init__(self, msg: str, lineno: int | None = None, token: str | None = None):
        super().__init__(msg)
        self.message = msg
        self.lineno = lineno
        self.token = token

    def __str__(self) -> str:
        msg = "Error"
        if self.lineno is not None:
            msg += f" [line {self.lineno}]"
        if self.token:
            msg += f" at {self.token!r}"
        msg += f": {self.message}"
        return msg


class LoxCallable(abc.ABC):
    @abc.abstractmethod
    def n_args(self) -> int: ...

    @abc.abstractmethod
    def call(self, args: list[LoxValue]) -> LoxValue: ...

    @abc.abstractmethod
    def name(self) -> str: ...


@dataclass
class PyFunction(LoxCallable):
    implementation: Callable[..., LoxValue]
    arity: int

    def name(self) -> str:
        return "builtin fn"

    def n_args(self) -> int:
        return self.arity

    def call(self, args: list[LoxValue]) -> LoxValue:
        return self.implementation(*args)


@dataclass
class LoxFunction(LoxCallable):
    ast: Function
    env: Env

    def name(self) -> str:
        return self.ast.name

    def n_args(self) -> int:
        return len(self.ast.args)

    def call(self, args: list[LoxValue]) -> LoxValue:
        arg_names = self.ast.args
        arg_map = dict(zip(arg_names, args))
        inner_env = self.env.child()
        for k, v in arg_map.items():
            inner_env.declare(k, v)

        try:
            for stmt in self.ast.body:
                interpreter.exec(stmt, inner_env)
        except LoxReturn as e:
            return e.value
        return None


class LoxReturn(Exception):
    def __init__(self, value):
        super().__init__(value)
        self.value = value


class Env(MutableMapping[str, LoxValue]):
    def __init__(
        self,
        parent: Env | None = None,
        data: dict[str, LoxValue] | None = None,
    ):
        if data is None:
            data = {}
        self._data = data
        self._parent = parent

    def __iter__(self) -> Iterator[str]:
        """obj.__iter__()  <==>  iter(obj)"""
        return iter(self._data)

    def __len__(self) -> int:
        """obj.__len__()  <==>  len(obj)"""
        return sum(1 for _ in self)

    def __getitem__(self, key: str) -> LoxValue:
        """obj.__getitem__(key)  <==>  obj[key]"""

        try:
            return self._data[key]
        except KeyError:
            if self._parent is None:
                raise
        return self._parent[key]

    def __setitem__(self, key: str, value: LoxValue):
        """obj.__setitem__(key, value)  <==>  obj[key] = value"""
        self._data[key] = value

    def __delitem__(self, key: str):
        """obj.__delitem__(key)  <==>  del obj[key]"""
        del self._data[key]

    def declare(self, var_name: str, value: LoxValue = None) -> None:
        if var_name in self._data:
            raise LoxError(f"redeclaração de variável: {var_name}")
        self._data[var_name] = value

    def assign(self, var_name: str, value: LoxValue) -> LoxValue:
        if var_name not in self._data:
            if self._parent is None:
                raise LoxError(f"variável não declarada: {var_name}")
            return self._parent.assign(var_name, value)
        else:
            self._data[var_name] = value
            return value

    def read_at(self, name: str, scope: int) -> LoxValue:
        if scope <= 0:
            try:
                return self._data[name]
            except KeyError:
                raise LoxError("variável indefinida: {name}")
        elif self._parent is None:
            raise LoxError("variável indefinida: {name}")
        else:
            return self._parent.read_at(name, scope - 1)

    def assign_at(self, name: str, scope: int, value: LoxValue) -> LoxValue:
        if scope <= 0:
            self._data[name] = value
            return value
        elif self._parent is None:
            raise RuntimeError(f"escopo inválido para {name}")
        else:
            return self._parent.assign_at(name, scope - 1, value)

    def child(self):
        return Env(self)
