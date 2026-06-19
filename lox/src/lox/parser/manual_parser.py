from dataclasses import dataclass
from typing import Any, Never, cast

from ..ast import Assign, Block, If, Name, Operator, Program, Var
from ..ast import Stmt, Print, ExprStmt, While
from ..ast import Expr, Literal, BinOp
from ..token import Token, TokenType
from ..scanner import lex


def parse(source: str) -> Program:
    tokens = lex(source)
    parser = LoxParser(tokens)
    program = parser.program()
    # Verifica se leu a lista de tokens até o final?
    return program


@dataclass
class LoxParser:
    tokens: list[Token]
    index: int = 0

    #
    # Regras da gramática
    #
    def program(self) -> Program:
        stmts = []
        while self.peek().kind != "EOF":
            stmt = self.declaration()
            stmts.append(stmt)
        return Program(stmts)

    def declaration(self) -> Stmt:
        match self.peek().kind:
            case "class":
                return self.not_implemented("class_decl")
            case "fun":
                return self.not_implemented("fun_decl")
            case "var":
                return self.var_decl()
            case _:
                return self.statement()

    def statement(self) -> Stmt:
        match self.peek().kind:
            case "if":
                return self.if_stmt()
            case "for":
                return self.not_implemented("for_stmt")
            case "while":
                return self.while_stmt()
            case "print":
                return self.print_stmt()
            case "return":
                return self.not_implemented("return_stmt")
            case "{":
                return self.block_stmt()
            case _:
                expr = self.expression()
                self.expect(";")
                return ExprStmt(expr)

    def print_stmt(self) -> Print:
        self.expect("print")
        expr = self.expression()
        self.expect(";")
        return Print(expr)

    def var_decl(self) -> Var:
        """
        'var' NAME ( '=' expr )? ';'
        """
        self.expect("var")
        name_token = self.expect("name")

        if self.peek().kind == "=":
            self.expect("=")
            expr = self.expression()
            self.expect(";")
        else:
            self.expect(";")
            expr = None

        return Var(name_token.lexeme, expr)

    def while_stmt(self) -> While:
        self.expect("while")
        self.expect("(")
        cond = self.expression()
        self.expect(")")

        stmt = self.statement()

        return While(cond, stmt)

    def if_stmt(self) -> If:
        self.expect("if")
        self.expect("(")
        cond = self.expression()
        self.expect(")")

        then = self.statement()

        or_else = None
        if self.match("else"):
            or_else = self.statement()

        return If(cond, then, or_else)

    def block_stmt(self):
        self.expect("{")

        stmts = []
        while self.peek().kind != "}":
            stmt = self.declaration()
            stmts.append(stmt)
        self.expect("}")

        return Block(stmts)

    def expression(self) -> Expr:
        return self.assignment()

    def assignment(self) -> Expr:
        """
        ( call "." )? IDENTIFIER "=" assignment | logic_or ;
        """

        if self.peek_next().kind == "=":
            name = self.expect("name")
            self.expect("=")
            right = self.assignment()
            return Assign(name.lexeme, right)
        else:
            return self.math_expr()

    def math_expr(self) -> Expr:
        value = self.term()

        while self.peek().kind in ("+", "-"):
            op = self.read()
            right = self.term()
            value = BinOp(value, cast(Operator, op.kind), right)

        return value

    def term(self) -> Expr:
        value = self.atom()

        while self.peek().kind in ("*", "/"):
            op = self.read()
            right = self.atom()
            value = BinOp(value, cast(Operator, op.kind), right)

        return value

    def atom(self) -> Expr:
        token = self.read()
        match token.kind:
            case "string" | "number" | "bool" | "nil":
                return Literal(token.value)
            case "name":
                return Name(token.lexeme)
            case _:
                self.error(f"átomo inválido: {token.kind}")

    def not_implemented(self, rule: str) -> Any:
        raise NotImplementedError(f"regra {rule} não-implementada")

    #
    # Métodos auxiliares
    #
    def peek(self) -> Token:
        try:
            return self.tokens[self.index]
        except IndexError:
            return Token("", "INVALID", -1)

    def peek_next(self) -> Token:
        try:
            return self.tokens[self.index + 1]
        except IndexError:
            return Token("", "INVALID", -1)

    def match(self, kind: TokenType) -> bool:
        if self.peek().kind == kind:
            self.read()
            return True
        return False

    def read(self) -> Token:
        token = self.peek()
        self.index += 1
        return token

    def expect(self, kind: TokenType) -> Token:
        token = self.peek()
        if token.kind != kind:
            self.error(f"esperava {kind}", token)
        else:
            self.index += 1
            return token

    def error(self, msg: str, token: Token | None = None) -> Never:
        if token:
            msg = f"linha {token.line} em '{token.lexeme}': {msg}"
        raise SyntaxError(msg)

