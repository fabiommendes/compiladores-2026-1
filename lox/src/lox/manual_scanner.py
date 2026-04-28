import string
from dataclasses import dataclass, field
from typing import cast

from .token import RESERVED_WORDS, Token, TokenType

LETTERS = set(string.ascii_letters + "_")
NUMBERS = set("0123456789")
ALPHAS = {*LETTERS, *NUMBERS}


@dataclass
class Lexer:
    source: str
    pos: int = 0
    index: int = 0
    line: int = 1
    tokens: list[Token] = field(default_factory=list)

    def add_token(self, kind: TokenType, *, value=None) -> Token:
        lexeme = self.source[self.pos : self.index]
        token = Token(lexeme, kind, self.line, value)
        self.tokens.append(token)
        self.pos = self.index
        return token

    def lex(self) -> list[Token]:
        while char := self.read():
            match char:
                case "{" | "}" | "(" | ")" | ";" | "," | "+" | "-" | "*" | ".":
                    self.add_token(cast(TokenType, char))
                case "/":
                    if self.peek() == "/":
                        self.skip_line()  # pula a linha de comentário
                    else:
                        self.add_token("/")
                case "=":
                    if self.peek() == "=":
                        self.read()
                        self.add_token("==")
                    else:
                        self.add_token("=")
                case "<":
                    if self.peek() == "=":
                        self.read()
                        self.add_token("<=")
                    else:
                        self.add_token("<")
                case ">":
                    if self.peek() == "=":
                        self.read()
                        self.add_token(">=")
                    else:
                        self.add_token(">")
                case "!":
                    if self.peek() == "=":
                        self.read()
                        self.add_token("!=")
                    else:
                        self.add_token("!")
                case '"':
                    self.add_string()
                case "\n":
                    self.line += 1
                    self.pos = self.index
                case " " | "\t" | "\r":
                    self.pos = self.index
                case "":
                    break
                case _ if char in LETTERS:
                    self.add_name()
                case _ if char in NUMBERS:
                    self.add_number()
                case _:
                    self.add_token("INVALID")

        self.tokens.append(Token("", "EOF", self.line))
        return self.tokens

    def read(self):
        char = self.peek()
        self.index += 1
        return char

    def peek(self):
        try:
            return self.source[self.index]
        except IndexError:
            return ""

    def add_string(self):
        try:
            self.index = self.source.index('"', self.index) + 1
        except ValueError:
            self.index = len(self.source)
            self.add_token("INVALID")
        else:
            token = self.add_token("string")
            token.value = token.lexeme[1:-1]
            self.line += token.lexeme.count("\n")

    def add_name(self):
        self.index = self.pos
        while self.source[self.index] in ALPHAS:
            self.index += 1

        token = self.add_token("name")

        if token.lexeme in RESERVED_WORDS:
            token.kind = token.lexeme
        elif token.lexeme == "true":
            token.kind = "bool"
            token.value = True
        elif token.lexeme == "false":
            token.kind = "bool"
            token.value = False
        elif token.lexeme == "nil":
            token.kind = "nil"
            token.value = None

    def add_number(self):
        self.index = self.pos

        while self.source[self.index] in NUMBERS:
            self.index += 1

        if self.source[self.index] == "." and self.source[self.index + 1] in NUMBERS:
            self.index += 1

            while self.source[self.index] in NUMBERS:
                self.index += 1

        token = self.add_token("number")
        token.value = float(token.lexeme)

    def skip_line(self):
        self.pos = self.source.find("\n", self.pos) + 1
        self.index = self.pos
        self.line += 1


def lex(source: str) -> list[Token]:
    lexer = Lexer(source + "\n")
    return lexer.lex()
