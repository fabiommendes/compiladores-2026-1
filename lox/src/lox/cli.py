import sys
import rich

from .scanner import lex

def main():
    if len(sys.argv) != 2:
        rich.print("[red b]ERRO:[/] digite lox NOME_DO_ARQUIVO")
        exit(1)

    path = sys.argv[1]
    with open(path) as f:
        source = f.read()

    tokens = lex(source)
    rich.print(tokens)
    ...
    # ast = parse(tokens)
    # inpret(ast)