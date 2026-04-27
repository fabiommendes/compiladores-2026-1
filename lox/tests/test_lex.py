try:
    from lox.re_scanner import lex
except ImportError:
    from lox.scanner import lex

def lexemes(src: str):
    tokens = [token.lexeme for token in lex(src)]
    tokens.pop()
    return tokens

def test_lex_hello_world():
    assert lexemes('print "Hello World";') == ["print_", '"Hello World"', ";"]