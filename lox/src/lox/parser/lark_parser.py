import rich

from lark import Lark, Token, Transformer, v_args
from pathlib import Path
from ..ast import (
    Assign,
    BinOp,
    Block,
    Call,
    Expr,
    ExprStmt,
    Function,
    Literal,
    If,
    Name,
    Operator,
    Print,
    Program,
    Return,
    Stmt,
    Var,
    While,
)

GRAMMAR: str = (Path(__file__).parent / "grammar.lark").read_text()


def parse(source: str) -> Program:
    grammar = Lark(GRAMMAR, start="program", parser="lalr")
    tree = grammar.parse(source)
    # print(tree.pretty())
    transformer = LoxTransformer()
    ast = transformer.transform(tree)
    # rich.print(ast)
    # exit()
    return ast


def bin_op_factory(op: Operator):
    def bin_op(self, left: Expr, right: Expr):
        return BinOp(left, op, right)

    return bin_op


@v_args(inline=True)
class LoxTransformer(Transformer):
    # EXPRESSOES
    add = bin_op_factory("+")
    sub = bin_op_factory("-")
    mul = bin_op_factory("*")
    div = bin_op_factory("/")
    pow = bin_op_factory("^")

    gt = bin_op_factory(">")
    lt = bin_op_factory("<")
    ge = bin_op_factory(">=")
    le = bin_op_factory("<=")
    eq = bin_op_factory("==")
    ne = bin_op_factory("!=")

    def assignment(self, name: Token, right: Expr):
        return Assign(str(name), right)

    def call(self, callee: Expr, args: list[Expr] | None = None):
        if args is None:
            args = []
        return Call(callee, args)

    def args(self, *args: Expr) -> list[Expr]:
        return list(args)

    def identifier(self, name: Token) -> Name:
        return Name(str(name), line_no=name.line)

    def number(self, value: Token) -> Literal:
        return Literal(float(value))

    def string(self, value: Token) -> Literal:
        return Literal(value[1:-1])

    def bool(self, value: Token) -> Literal:
        return Literal(value == "true")

    def nil(self) -> Literal:
        return Literal(None)

    # COMANDOS
    def print_stmt(self, expr: Expr):
        return Print(expr)

    @v_args(inline=False)
    def program(self, stmts: list[Stmt]):
        return Program(stmts)

    @v_args(inline=False)
    def block(self, stmts: list[Stmt]):
        return Block(stmts)

    def var_decl(self, name: Token, right: Expr | None = None):
        return Var(str(name), right, line_no=name.line)

    def while_stmt(self, cond: Expr, body: Stmt):
        return While(cond, body)

    def if_stmt(self, cond: Expr, body: Stmt, or_else: Stmt | None = None):
        return If(cond, body, or_else)

    def expression_stmt(self, expr: Expr):
        return ExprStmt(expr)

    def method(self, name: Token, params: list[str], body: Block):
        return Function(str(name), params, body.stmts)

    def params(self, *names: Token) -> list[str]:
        return [str(token) for token in names]

    def return_stmt(self, expr: Expr | None = None) -> Return:
        return Return(expr)
