"""
Exemplo de uso de regex para criar um roteador simples que mapeia URLs para
funções.

Algo parecido com isso pode ser usado em um framework web para lidar com
requisições HTTP, ou em uma CLI para mapear comandos para funções. 

Nosso micro(semi)-framework é composto por duas funções:

- `route(pattern: str)`: decorador que registra as rotas criadas pelo usuário.
- `dispatch(url: str)`: recebe uma URL e executa a função correspondente de
  acordo com as rotas registradas. 
  
"""

from typing import Pattern, Callable
import re

ROUTES: dict[Pattern, Callable] = {}


def route(pattern: str):
    """
    Decorador para registrar uma função como manipuladora de uma URL que
    corresponda a um padrão regex. O padrão é compilado e armazenado no
    dicionário ROUTES, associando-o à função decorada.
    """
    def decorator(func: Callable) -> Callable:
        ROUTES[re.compile(pattern)] = func
        return func
    return decorator


def dispatch(url: str):
    """
    Recebe uma URL e tenta encontrar uma função correspondente no dicionário
    ROUTES. Para cada regex registrada, ele tenta fazer um fullmatch com a URL.
    Se houver uma correspondência, ele extrai os grupos nomeados (se houver) e
    os passa como argumentos para a função correspondente.
    """
    for regex, func in ROUTES.items():
        m = regex.fullmatch(url)
        if m is None:
            continue

        kwargs = m.groupdict()
        if not kwargs:
            args = m.groups()
            return func(*args)

        return func(**kwargs)

    print("Error 404: url nao encontrada")



# ==============================================================================
# Exemplos de rotas registradas com o decorador route.
# 
# Este seria o código de aplicação que usa o nosso "framework".
# ==============================================================================
@route(r"/api/v1/users/?")
def user_list():
    user_detail("fulano")
    user_detail("cicrano")
    user_detail("beltrano")

@route(r"/api/v1/users/(?P<username>\w+)/?")
def user_detail(username: str):
    print(f"User: {username}")

@route(r"/auth/login/?")
def login_page():
    print("Login page")

@route(r"/actions/add/(\d+)\+(\d+)/?")
def add(x, y):
    result = int(x) + int(y)
    print("add:", result)

@route(r"/(?P<username>\w+)/(?P<repo>\w+)/?")
def repo_page(username, repo):
    print(f"Repo: {username}/{repo}")


# ==============================================================================
# No loop principal do programa, podemos dispachar URLs para as funções 
# registradas usando o roteador.
# ==============================================================================
if  __name__ == "__main__":
    while True:
        try:
            url = input("url: ")
        except (SystemExit, EOFError):
            break
        dispatch(url)