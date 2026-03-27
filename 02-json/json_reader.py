import sys
import pprint
from typing import Literal
from dataclasses import dataclass

type JSON = str | int | float | bool | None | list | dict
type TokenType = Literal[
    "NUM",
    "STR",
    "LIT",
    "OPEN_LIST",
    "CLOSE_LIST",
    "COMMA",
    "OPEN_OBJECT",
    "CLOSE_OBJECT",
    "COLON",
    "EOF",
]

LIT_VALUE = {
    "true": True,
    "false": False,
    "null": None,
}

@dataclass
class Token:
    text: str
    kind: TokenType

def main():
    file_name = sys.argv[-1]

    with open(file_name) as f:
        source = f.read()

    value = parse(source)
    pprint.pprint(value)


def parse(src: str) -> JSON:
    tokens = lex(src + " ")
    tokens.append(Token("", "EOF"))
    tokens.reverse()

    result = value(tokens)
    assert tokens == [Token("", "EOF")]
    return result


def value(tokens: list[Token]) -> JSON:
    match tokens.pop():
        case Token(text, "NUM"):
            return int(text)
        case Token(text, "STR"):
            return text[1:-1]
        case Token(text, "LIT"):
            return LIT_VALUE[text]
        case Token(_, "OPEN_LIST"):
            return array(tokens)
        case Token(_, "OPEN_LIST"):
            return array(tokens)
        case Token(_, "OPEN_OBJECT"):
            return object(tokens)
        case _:
            raise SyntaxError(tokens)

def array(tokens: list[Token]) -> list:
    elems = []
    while tokens[-1].kind != "CLOSE_LIST":
        elems.append(value(tokens))

        if tokens[-1].kind == "COMMA":
            tokens.pop()
        elif tokens[-1].kind != "CLOSE_LIST":
            raise SyntaxError

    assert tokens.pop().kind == "CLOSE_LIST"
    return elems

def object(tokens: list[Token]) -> list:
    elems = []
    while tokens[-1].kind != "CLOSE_OBJECT":
        elems.append(pair(tokens))

        if tokens[-1].kind == "COMMA":
            tokens.pop()
        elif tokens[-1].kind != "CLOSE_OBJECT":
            raise SyntaxError

    assert tokens.pop().kind == "CLOSE_OBJECT"
    return dict(elems)

def pair(tokens: list[Token]) -> tuple[str, JSON]:
    # Le string como chave
    tk = tokens.pop()
    assert tk.kind == "STR"
    key = tk.text[1:-1]

    # Le o dois pontos
    tk = tokens.pop()
    assert tk.kind == "COLON"

    # Le e retorna o valor
    return key, value(tokens)

def lex(src: str) -> list[Token]:
    tokens: list[Token] = []

    idx = 0
    while idx < len(src):
        match src[idx]:
            case " " | "\n" | "\t" | "\r":
                idx += 1
            case '"':
                idx, tk = read_string(src, idx)
                tokens.append(tk)
            case "[":
                idx += 1
                tokens.append(Token("[", "OPEN_LIST"))
            case "]":
                idx += 1
                tokens.append(Token("]", "CLOSE_LIST"))
            case "{":
                idx += 1
                tokens.append(Token("{", "OPEN_OBJECT"))
            case "}":
                idx += 1
                tokens.append(Token("}", "CLOSE_OBJECT"))
            case ",":
                idx += 1
                tokens.append(Token(",", "COMMA"))
            case ":":
                idx += 1
                tokens.append(Token(":", "COLON"))
            case "-":
                idx, tk = read_number(src, idx + 1)
                tk.text = "-" + tk.text
                tokens.append(tk)
            case "n" if src[idx:idx + 4] == "null":
                idx += 4
                tokens.append(Token("null", "LIT"))
            case "t" if src[idx : idx + 4] == "true":
                idx += 4
                tokens.append(Token("true", "LIT"))
            case "f" if src[idx : idx + 5] == "false":
                idx += 5
                tokens.append(Token("false", "LIT"))
            case n if n.isdigit():
                idx, tk = read_number(src, idx)
                tokens.append(tk)
            case _:
                raise SyntaxError(src[idx:])

    return tokens

def read_string(src: str, i: int):
    j = src.index('"', i + 1)
    return j + 1, Token(src[i:j + 1], "STR")

def read_number(src: str, i: int):
    j = i
    while src[j].isdigit():
        j += 1
    return j, Token(src[i:j], "NUM")


if __name__ == "__main__":
    main()
