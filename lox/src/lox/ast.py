from __future__ import annotations

from dataclasses import dataclass
from typing import Literal as LiteralType

type Operator = LiteralType[
    "+",
    "-",
    "*",
    "/",
    "^",
    ">",
    "<",
    ">=",
    "<=",
    "==",
    "!=",
]

type LoxPrimitive = str | float | bool | None

type Scope = int


@dataclass
class Program:
    stmts: list[Stmt]


# ==============================================================================
# Expressões
# ==============================================================================
type Expr = Literal | BinOp | Name | Assign | Call


@dataclass
class Literal:
    value: LoxPrimitive


@dataclass
class Name:
    name: str
    scope: Scope | None = None
    line_no: int = 0


@dataclass
class BinOp:
    left: Expr
    op: Operator
    right: Expr
    line_no: int = 0


@dataclass
class Assign:
    name: str
    right: Expr
    scope: Scope | None = None
    line_no: int = 0


@dataclass
class Call:
    callee: Expr
    args: list[Expr]


...


# ==============================================================================
# Comandos e declarações
# ==============================================================================
type Stmt = Print | While | If | ExprStmt | Var | Block | Function | Return  # ...


@dataclass
class Print:
    expr: Expr


@dataclass
class While:
    cond: Expr
    stmts: Stmt


@dataclass
class If:
    cond: Expr
    then: Stmt
    or_else: Stmt | None


@dataclass
class ExprStmt:
    expr: Expr


@dataclass
class Var:
    name: str
    right: Expr | None = None
    line_no: int = 0


@dataclass
class Block:
    stmts: list[Stmt]


@dataclass
class Function:
    name: str
    args: list[str]
    body: list[Stmt]


@dataclass
class Return:
    expr: Expr | None


...
