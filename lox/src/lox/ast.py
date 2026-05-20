from __future__ import annotations

from dataclasses import dataclass
from typing import Literal as LiteralType

type Operator = LiteralType["+", "-", "*", "/"]
type LoxValue = str | float | bool | None


@dataclass
class Program:
    stmts: list[Stmt]


# ==============================================================================
# Expressões
# ==============================================================================
type Expr = Literal | BinOp | Name | Assign


@dataclass
class Literal:
    value: str | float | bool | None


@dataclass
class Name:
    name: str


@dataclass
class BinOp:
    left: Expr
    op: Operator
    right: Expr


@dataclass
class Assign:
    name: str
    right: Expr


...


# ==============================================================================
# Comandos e declarações
# ==============================================================================
type Stmt = Print | While | If | ExprStmt | Var | Block  # ...


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


@dataclass
class Block:
    stmts: list[Stmt]


...
