from .ast import Assign, Block, ExprStmt, If, Program, LoxValue, Operator, Var
from .ast import Expr, BinOp, Literal, Name
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

        case Name(name):
            return env[name]

        case Assign(name, right):
            env[name] = value = eval(right, env)
            return value

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
            env[name] = value

        case Block(stmts):
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
