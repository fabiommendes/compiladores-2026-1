from .interpreter import interpret
from .parser import parse
from .scanner import lex
from .token import Token, TokenType

__all__ = [
    "interpret",
    "lex",
    "parse",
    "run_source",
    "Token",
    "TokenType",
]


def run_source(source: str) -> None:
    tokens = lex(source)
    ast = parse(tokens)
    interpret(ast)
