from dataclasses import dataclass
from typing import Any, Never, cast

from .ast import Operator, Program
from .ast import Stmt, Print, ExprStmt, While
from .ast import Expr, Literal, BinOp
from .token import Token, TokenType


def parse(tokens: list[Token]) -> Program:
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
            stmt = self.statement()
            stmts.append(stmt)
        return Program(stmts)

    def statement(self) -> Stmt:
        match self.peek().kind:
            case "class":
                return self.not_implemented("class_decl")
            case "fun":
                return self.not_implemented("fun_decl")
            case "var":
                return self.not_implemented("var_decl")
            case "if":
                return self.not_implemented("if_stmt")
            case "for":
                return self.not_implemented("for_stmt")
            case "while":
                return self.while_stmt()
            case "print":
                return self.print_stmt()
            case "return":
                return self.not_implemented("return_stmt")
            case "{":
                return self.not_implemented("block_stmt")
            case _:
                expr = self.expression()
                self.expect(";")
                return ExprStmt(expr)

    def print_stmt(self) -> Print:
        self.expect("print")
        expr = self.expression()
        self.expect(";")
        return Print(expr)

    def while_stmt(self) -> While:
        self.expect("while")
        self.expect("(")
        cond = self.expression()
        self.expect(")")

        self.expect("{")
        stmts = []
        while self.peek().kind != "}":
            stmt = self.statement()
            stmts.append(stmt)
        self.expect("}")

        return While(cond, stmts)

    def expression(self) -> Expr:
        # FIXME
        return self.math_expr()

    def math_expr(self) -> Expr:
        value = self.term()

        while self.peek().kind  in ("+", "-"):
            op = self.read()
            right = self.term()
            value = BinOp(value, cast(Operator, op.kind), right)

        return value

    def term(self) -> Expr:
        value = self.atom()

        while self.peek().kind  in ("*", "/"):
            op = self.read()
            right = self.atom()
            value = BinOp(value, cast(Operator, op.kind), right)

        return value

    def atom(self) -> Expr:
        token = self.read()
        if token.kind not in ("string", "number", "bool", "nil"):
            self.error(f"átomo inválido: {token.kind}")
        return Literal(token.value)

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
