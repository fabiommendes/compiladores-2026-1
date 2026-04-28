from dataclasses import dataclass
from typing import Literal

type TokenType = Literal[
    # Básicos
    "name",
    "string",
    "number",
    "bool",
    "nil",
    # Palavras reservadas
    "if",
    "else",
    "while",
    "for",
    "print",
    "class",
    "fun",
    "return",
    "this",
    "super",
    "var",
    "and",
    "or",
    # Símbolos especiais
    ";",
    "{",
    "}",
    "(",
    ")",
    "+",
    "-",
    "/",
    "*",
    # Comparações
    "=",
    "==",
    "!=",
    "!",
    ">",
    ">=",
    "<",
    "<=",
    # ...
    # Tokens fictícios
    "EOF",
    "INVALID",
]

RESERVED_WORDS: set[TokenType] = {
    "if",
    "else",
    "while",
    "for",
    "print",
    "class",
    "fun",
    "return",
    "this",
    "var",
    "super",
    "and",
    "or",
}

LITERALS: dict[str, TokenType] = {"true": "bool", "false": "bool", "nil": "nil"}


@dataclass
class Token:
    lexeme: str
    kind: TokenType
    line: int
    value: float | bool | str | None = None
