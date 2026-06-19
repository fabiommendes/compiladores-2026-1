from __future__ import annotations
import math
import time
from typing import assert_never, cast

from .ast import (
    ExprStmt,
    Function,
    If,
    Program,
    Operator,
    Return,
    Var,
)
from .ast import Assign, Call, Expr, BinOp, Literal, Name
from .ast import Stmt, Print, While, Block

from .runtime import (
    Env,
    LoxCallable,
    LoxError,
    LoxFunction,
    LoxReturn,
    LoxValue,
    PyFunction,
)


def read_string(prompt):
    return input(prompt)


def read_number(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Digite um número válido")
        return read_number(prompt)


def new_env() -> Env:
    env = Env()
    env.declare("clock", PyFunction(time.time, 0))
    env.declare("sqrt", PyFunction(math.sqrt, 1))
    env.declare("read_number", PyFunction(read_number, 1))
    env.declare("read_string", PyFunction(read_string, 1))
    return env


def interpret(program: Program):
    env = new_env()
    try:
        for stmt in program.stmts:
            exec(stmt, env)
    except LoxError as e:
        print(e)


def eval(expr: Expr, env: Env) -> LoxValue:
    match expr:
        case Literal(value):
            return value

        case BinOp(left, op, right):
            left_value = eval(left, env)
            right_value = eval(right, env)
            return apply_operator(op, left_value, right_value)

        case Name(name, scope):
            return env.read_at(name, cast(int, scope))

        case Assign(name, right, scope):
            return env.assign_at(name, cast(int, scope), eval(right, env))

        case Call(callee, args):
            function = eval(callee, env)
            arg_values = [eval(arg, env) for arg in args]

            if not isinstance(function, LoxCallable):
                kind = type(function).__name__
                raise LoxError(f"objeto {kind} não é uma função")
            elif function.n_args() != len(arg_values):
                msg = f"{function.name()} espera {function.n_args()} argumentos."
                raise LoxError(msg)
            else:
                return function.call(arg_values)

        case _:
            type_name = type(expr).__name__
            raise ValueError(f"tipo não suportado: {type_name}")


def exec(cmd: Stmt, env: Env):
    match cmd:
        case Print(expr):
            value = eval(expr, env)
            print(value)

        case While(cond, stmt):
            while eval(cond, env):
                exec(stmt, env)

        case If(cond, then, or_else):
            if eval(cond, env):
                exec(then, env)
            elif or_else is not None:
                exec(or_else, env)

        case ExprStmt(expr):
            eval(expr, env)

        case Var(name, right):
            value = eval(right, env) if right is not None else None
            env.declare(name, value)

        case Block(stmts):
            child_env = env.child()
            for stmt in stmts:
                exec(stmt, child_env)

        case Function(name, _, _):
            env.declare(name, LoxFunction(cmd, env))

        case Return(expr):
            if expr is None:
                raise LoxReturn(None)
            raise LoxReturn(eval(expr, env))

        case _:
            type_name = type(cmd).__name__
            raise ValueError(f"tipo não suportado: {type_name}")


def apply_operator(op: Operator, x, y):
    match op:
        case "+":
            return x + y
        case "-":
            return x - y
        case "*":
            return x * y
        case "/":
            return x / y
        case "^":
            return x**y
        case ">":
            return x > y
        case "<":
            return x < y
        case ">=":
            return x >= y
        case "<=":
            return x <= y
        case "==":
            return x == y
        case "!=":
            return x != y

        case _:
            assert_never(op)
