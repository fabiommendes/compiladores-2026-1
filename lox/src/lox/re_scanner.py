import string
import re
from typing import cast

from .token import Token, TokenType

LETTERS = set(string.ascii_letters + "_")
NUMBERS = set("0123456789")
ALPHAS = {*LETTERS, *NUMBERS}
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
}

NUMBER = re.compile(r"\d+")

TOKEN_PATTERNS = {
    "comment": r"//[^\n]*",
    "name": r"[a-zA-Z_][a-zA-Z_0-9]*",
    "string": r'"[^"]*"',
    "symbol": r"==|!=|>=|<=|[<>+/*;={}(),.-]",
    "space": r"\s+",
    "number": r"[0-9]+(\.[0-9]+)?",
    # Importante que seja a última regra
    "INVALID": r".",
}

LITERAL_VALUES = {
    "true": True,
    "false": False,
    "nil": None,
}

LITERAL_TYPES: dict[str, TokenType] = {
    "true": "bool",
    "false": "bool",
    "nil": "nil",
}

LOX_RE = re.compile(
    "|".join(f"(?P<{key}>{value})" for key, value in TOKEN_PATTERNS.items())
)

def lex(source: str) -> list[Token]:
    tokens: list[Token] = []
    line = 1

    for m in LOX_RE.finditer(source):
        i, j = m.span()
        lexeme = source[i:j]
        kind = cast(TokenType, m.lastgroup or "INVALID")
        token = Token(lexeme, kind, line)
        tokens.append(token)

        match kind:
            case "space" | "comment":
                tokens.pop()
                line += lexeme.count("\n")
            case "name":
                if lexeme in RESERVED_WORDS:
                    token.kind = cast(TokenType, lexeme)
                if lexeme in LITERAL_VALUES:
                    token.kind = LITERAL_TYPES[lexeme]
                    token.value = LITERAL_VALUES[lexeme]
            case "symbol":
                token.kind = lexeme
            case "string":
                token.value = lexeme[1:-1]
                line += lexeme.count("\n")
            case "number":
                token.value = float(lexeme)
            case _:
                pass

    tokens.append(Token("", "EOF", line))
    return tokens