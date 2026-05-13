from .ast import Program, LoxValue, Operator
from .ast import Expr, BinOp, Literal
from .ast import Stmt, Print, While
from typing import assert_never

type Env = dict[str, LoxValue]


def new_env() -> Env:
    return {}


def interpret(program: Program):
    env = new_env()
    for stmt in program.stmts:
        exec(stmt, env)


def eval(expr: Expr, env: Env) -> LoxValue:
    match expr:
        case Literal(value):
            return value

        case BinOp(left, op, right):
            left_value = eval(left, env)
            right_value = eval(right, env)
            return apply_operator(op, left_value, right_value)

        case _:
            type_name = type(expr).__name__
            raise ValueError(f"tipo não suportado: {type_name}")


def exec(cmd: Stmt, env: Env):
    match cmd:
        case Print(expr):
            value = eval(expr, env)
            print(value)

        case While(cond, stmts):
            while eval(cond, env):
                for stmt in stmts:
                    exec(stmt, env)

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
        case _:
            assert_never(op)
