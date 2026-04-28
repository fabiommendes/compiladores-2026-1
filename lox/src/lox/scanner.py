"""
Scanner.

Importamos a função `lex` do módulo `re_scanner`, mas podemos mudar o scanner
padrão usando variáveis de ambiente.

Se iniciarmos o programa com `LOX_SCANNER=manual uv run lox <arquivo>`, a
implementação usará o scanner manual.
"""

import os

__all__ = ["lex"]

if os.environ.get("LOX_SCANNER") == "manual":
    from .manual_scanner import lex
else:
    from .re_scanner import lex
