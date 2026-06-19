from hypothesis.extra.lark import from_lark
from lark import Lark

with open("lox.lark") as f:
    grammar = Lark(f.read(), start="program")
grammar_st = from_lark(grammar, start="program")

# for _ in range(5):
print(grammar_st.example())
print("\n\n")
