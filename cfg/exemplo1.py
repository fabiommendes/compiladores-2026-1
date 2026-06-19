from typing import Callable, TypeGuard

from lark import Lark, LarkError
from random import choice

GRAMMAR = r"""
start : "(" elems ")"
      | ELEM

elems : start elems
      | // ε

ELEM  : /[ab]/
"""

type NonTerminal = str
type Terminal = Callable[[], str]
type GrammarRules = dict[NonTerminal, list[list[Terminal| NonTerminal]]]

grammar = Lark(GRAMMAR)

TOKEN = lambda x: lambda: x  # noqa: E731
ELEM = lambda: choice("ab")  # noqa: E731

def is_terminal(obj: Terminal | NonTerminal) -> TypeGuard[Terminal]:
    return callable(obj)

rules: GrammarRules = {
    "start": [
        [TOKEN("("), "elems", TOKEN(")")],
        [ELEM],
    ],
    "elems": [
        ["start", "elems"],
        [],
    ],
}

def generate(rules: GrammarRules, start: NonTerminal = "start") -> str:
    options = rules[start]
    option = choice(options)

    parts = []
    for symbol in option:
        if callable(symbol):
            parts.append(symbol())
        else:
            parts.append(generate(rules, symbol))

    return "".join(parts)


for _ in range(10):
    print(generate(rules))

# if __name__ == "__main__":
#     while (src := input("> ")):
#         try:
#             tree = grammar.parse(src)
#         except LarkError as ex:
#             print(f"erro: {ex}")
#         else:
#             print(tree.pretty())
