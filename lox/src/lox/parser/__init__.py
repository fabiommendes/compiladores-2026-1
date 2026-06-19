"""
Analisador sintático.

Importamos a função `parse` do módulo `lark_parser`, mas podemos mudar o parser
padrão usando variáveis de ambiente.

Se iniciarmos o programa com `LOX_PARSER=manual uv run lox <arquivo>`, a
implementação usará o parser manual.
"""

import os

__all__ = ["lex"]

if os.environ.get("LOX_PARSER") == "manual":
    from .manual_parser import parse
else:
    from .lark_parser import parse
