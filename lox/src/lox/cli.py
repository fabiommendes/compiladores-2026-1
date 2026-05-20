import os
import sys

import rich

from .interpreter import interpret
from .parser import parse
from .scanner import lex


def main():
    if len(sys.argv) != 2:
        rich.print("[red b]ERRO:[/] digite lox NOME_DO_ARQUIVO")
        exit(1)

    path = sys.argv[1]
    if not os.path.exists(path):
        rich.print(f"[red b]ERRO:[/] arquivo '{path}' não encontrado")
        exit(1)

    with open(path) as f:
        source = f.read()

    tokens = lex(source)
    ast = parse(tokens)
    interpret(ast)
