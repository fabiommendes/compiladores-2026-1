from __future__ import annotations
from typing import Any, Literal as Enum

from .ast import (
    ExprStmt,
    Function,
    If,
    Program,
    Return,
    Var,
)
from .ast import Assign, Call, Expr, BinOp, Literal, Name
from .ast import Stmt, Print, While, Block
from .runtime import LoxError


class Env:
    parent: Env | None
    fn_context: Enum["module", "function", "method"]
    errors: list[LoxError] | None
    variables: dict[str, Enum["declared", "reserved"]]

    def __init__(self, parent: Env | None = None):
        self.errors = None
        self.fn_context = "module"
        self.parent = parent
        self.variables = {}

    def declare(self, name: str) -> Any:
        self.variables[name] = "declared"

    def reserve(self, name: str) -> Any:
        self.variables[name] = "reserved"

    def assign(self, name: str) -> Any: ...

    def error(self, msg: str, lineno: int | None = None, token: str | None = None):
        error = LoxError(msg, lineno, token)
        if self.parent is not None:
            self.parent.error(msg, lineno)
        elif self.errors is None:
            self.errors = [error]
        else:
            self.errors.append(error)

    def child(self):
        return Env(self)

    def scope(self, name: str, lineno: int) -> int:
        if name in self.variables:
            if self.variables[name] == "reserved":
                self.error(f"{name!r} está sendo usada em sua definição.", lineno)
            return 0
        elif self.parent:
            return self.parent.scope(name, lineno) + 1
        else:
            return 0


def new_env() -> Env:
    env = Env()
    env.declare("clock")
    env.declare("sqrt")
    env.declare("read_number")
    env.declare("read_string")
    return env


def semantic_analysis(program: Program) -> list[LoxError]:
    env = new_env()
    for stmt in program.stmts:
        visit_cmd(stmt, env)
    return env.errors or []


def visit_expr(expr: Expr, env: Env):
    match expr:
        case Literal(_):
            ...

        case BinOp(left, _, right):
            visit_expr(left, env)
            visit_expr(right, env)

        case Name(name, line_no=line):
            expr.scope = env.scope(name, line)

        case Assign(name, right, line_no=line):
            visit_expr(right, env)
            env.assign(name)
            expr.scope = env.scope(name, line)

        case Call(callee, args):
            visit_expr(callee, env)
            for arg in args:
                visit_expr(arg, env)

        case _:
            type_name = type(expr).__name__
            raise ValueError(f"tipo não suportado: {type_name}")


def visit_cmd(cmd: Stmt, env: Env):
    match cmd:
        case Print(expr):
            visit_expr(expr, env)

        case While(cond, stmt):
            visit_expr(cond, env)
            visit_cmd(stmt, env)

        case If(cond, then, or_else):
            visit_expr(cond, env)
            visit_cmd(then, env)
            if or_else is not None:
                visit_cmd(or_else, env)

        case ExprStmt(expr):
            visit_expr(expr, env)

        case Var(name, right):
            env.reserve(name)
            if right is not None:
                visit_expr(right, env)
            env.declare(name)

        case Block(stmts):
            child_env = env.child()
            for stmt in stmts:
                visit_cmd(stmt, child_env)

        case Function(name, args, body):
            env.declare(name)
            body_env = env.child()
            body_env.fn_context = "function"
            for arg in args:
                body_env.declare(arg)
            for stmt in body:
                visit_cmd(stmt, body_env)

        case Return(expr):
            if env.fn_context == "module":
                env.error("return fora de função ou método")

            if expr is not None:
                visit_expr(expr, env)

        case _:
            type_name = type(cmd).__name__
            raise ValueError(f"tipo não suportado: {type_name}")
