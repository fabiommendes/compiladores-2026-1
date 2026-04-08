from typing import Literal
from dataclasses import dataclass

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

@dataclass
class Token:
    lexeme: str
    kind: TokenType
    line: int
    value: float | bool | str | None = None
