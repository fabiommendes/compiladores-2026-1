import os
import sys

import rich
from rich.console import Console
from rich.syntax import Syntax

from .interpreter import interpret
from . import interpreter
from .parser import parse
from .semantic import semantic_analysis


def main():
    args = sys.argv.copy()
    show_ast = extract_flag("--show-ast", args) or extract_flag("-a", args)
    show_code = extract_flag("--show-code", args) or extract_flag("-c", args)

    path = parse_args(args)
    if path is None:
        repl()
        return

    if not os.path.exists(path):
        rich.print(f"[red b]ERRO:[/] arquivo '{path}' não encontrado")
        exit(1)

    with open(path) as f:
        source = f.read()

    if show_code:
        syntax = Syntax(source, lexer="javascript", line_numbers=True)
        Console().print(syntax)
        return

    ast = parse(source)
    errors = semantic_analysis(ast)
    if errors:
        for error in errors:
            print(error)
    elif show_ast:
        rich.print(ast)
    else:
        interpret(ast)


def repl():
    env = interpreter.new_env()

    while True:
        try:
            source = input("> ")
            ast = parse(source)

            for stmt in ast.stmts:
                interpreter.exec(stmt, env)

        except (SystemExit, IOError):
            break

        except Exception as ex:
            print(f"Erro: {ex}")


def parse_args(args: list[str]) -> str | None:
    if len(args) == 1:
        return None
    elif len(args) == 2:
        return args[1]
    else:
        rich.print(
            "[red b]ERRO:[/] digite lox NOME_DO_ARQUIVO [--show-ast] [--show-code]"
        )
        exit(1)


def extract_flag(flag: str, args: list[str]) -> bool:
    """
    Verifica se a flag existe na lista de args, remove-a
    e retorna um booleano dizendo se a flag está definida ou não.
    """
    flag_exists = flag in args
    if flag_exists:
        args.remove(flag)
    return flag_exists