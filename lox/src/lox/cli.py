import sys

import rich

from .re_scanner import lex
from .parser import parse
from .interpreter import interpret



def main():
    if len(sys.argv) != 2:
        rich.print("[red b]ERRO:[/] digite lox NOME_DO_ARQUIVO")
        exit(1)

    path = sys.argv[1]
    with open(path) as f:
        source = f.read()

    tokens = lex(source)
    ast = parse(tokens)
    interpret(ast)
