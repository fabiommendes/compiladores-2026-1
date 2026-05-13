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
type Expr = Literal | BinOp


@dataclass
class Literal:
    value: str | float | bool | None


@dataclass
class BinOp:
    left: Expr
    op: Operator
    right: Expr


...


# ==============================================================================
# Comandos e declarações
# ==============================================================================
type Stmt = Print | While | ExprStmt  # ...


@dataclass
class Print:
    expr: Expr


@dataclass
class While:
    cond: Expr
    stmts: list[Stmt]


@dataclass
class ExprStmt:
    expr: Expr


...
