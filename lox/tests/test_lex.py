import threading
from pathlib import Path
from typing import Iterator
from unittest import TestCase

from lox.testing import Result, mod, read_example
from lox.token import RESERVED_WORDS, Token

TEST_BASE = Path(__file__).parent.parent / "exemplos" / "scanning"
KINDS = {
    "STRING": "string",
    "INT": "int",
    "NUMBER": "number",
    "IDENTIFIER": "name",
    # Símbolos especiais
    "DOT": ".",
    "COMMA": ",",
    "SEMICOLON": ";",
    "LEFT_BRACE": "{",
    "RIGHT_BRACE": "}",
    "LEFT_PAREN": "(",
    "RIGHT_PAREN": ")",
    "PLUS": "+",
    "MINUS": "-",
    "SLASH": "/",
    "STAR": "*",
    # Comparações
    "EQUAL": "=",
    "EQUAL_EQUAL": "==",
    "BANG_EQUAL": "!=",
    "BANG": "!",
    "GREATER": ">",
    "GREATER_EQUAL": ">=",
    "LESS": "<",
    "LESS_EQUAL": "<=",
    "FALSE": "bool",
    "TRUE": "bool",
    "NIL": "nil",
    **{word.upper(): word for word in RESERVED_WORDS},
}


class TestScanner(TestCase):
    def test_hello_world(self):
        src = 'print "Hello, World!";'
        tokens = tokenize(src)

        for token in tokens:
            print(token)

        assert tokens[0].kind == "print"
        assert tokens[1].kind == "string"
        assert tokens[1].value == "Hello, World!"
        assert tokens[2].kind in ("SEMICOLON", ";")
        assert tokens[3].kind in ("EOF", "eof")
        assert len(tokens) == 4

    def test_identifiers(self):
        check_scanner("identifier")

    def test_numbers(self):
        check_scanner("number")

    def test_strings(self):
        check_scanner("string")

    def test_reserved(self):
        check_scanner("reserved")

    def test_symbols(self):
        check_scanner("symbol")

    def test_spaces(self):
        check_scanner("space")


def check_scanner(file: str):
    path = TEST_BASE / f"{file}.lox"
    example = read_example(path)

    print(f"Análise léxica, {file}.lox")
    print(indent(strip_comments(example.source)))

    tokens = tokenize(example.source)
    print("\nTokens obtidos")

    iter_tokens = iter(tokens)
    iter_expected = iter(example.expect)

    for token, result in zip(iter_tokens, iter_expected):
        print(indent(f"* {token}"))
        print(indent(f"* {result}"), end="")

        # Processa strings com espaços corretamente
        kind, _, rest = result.message.partition(" ")
        if rest.startswith('"'):
            lexeme, sep, value = rest[1:].partition('"')
            value = value.lstrip()
            lexeme = '"' + lexeme + '"'
        else:
            lexeme, _, value = rest.partition(" ")

        msg = f"lexema: obteve {token.lexeme!r}, esperado {lexeme!r}"
        assert token.lexeme == lexeme, msg

        msg = f"tipo: obteve {token.kind!r}, esperado {kind!r}"
        assert token.kind == KINDS.get(kind, kind), msg

        if value != "null":
            msg = f"valor: obteve {token.value!r}, esperado {value!r}"
            assert str(token.value).removesuffix(".0") == value, msg

        print(" ...OK\n")

    consume_EOF(iter_tokens)
    consume_EOF(iter_expected)


def tokenize(src: str) -> list[Token]:
    lex = mod("scanner:lex")
    tokens = []

    thread = threading.Thread(target=lambda: tokens.extend(lex(src)))
    thread.start()
    thread.join(timeout=1.0)

    return tokens


def strip_comments(src: str) -> str:
    lines = src.splitlines()
    stripped_lines = []
    for line in lines:
        if "//" in line:
            line = line.split("//", 1)[0]
        if line:
            stripped_lines.append(line)
    return "\n".join(stripped_lines)


def indent(text: str, prefix: str = "    ") -> str:
    return "\n".join(prefix + line for line in text.splitlines())


def consume_EOF(items: Iterator[Token | Result]):
    for item in items:
        if isinstance(item, Token):
            assert item.kind in ("EOF", "eof"), f"token extra inesperado: {item!r}"
        else:
            msg = f"resultado extra inesperado: {item!r}"
            assert item.message.lower().startswith("eof"), msg


if __name__ == "__main__":
    import unittest

    unittest.main()
