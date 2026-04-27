"""
Exemplo de uso de regex para extrair informação sobre datas de uma string.
"""

import re
import datetime


# Criamos uma regex com dois formatos de data, usando grupos nomeados para 
# extrair os componentes da data. Note que usamos o modificador re.VERBOSE para 
# permitir que a regex seja escrita de forma mais legível, com comentários e 
# espaçamento. O modo verboso ignora espaços em branco e se quisermos usar um 
# espaço literal, precisamos escapá-lo com "\ " ou "[ ]".
DATE_REGEX = re.compile(r"""
    # Formato padrao
    (?P<day>[0-9]{1,2})/(?P<month>[0-9]{1,2})/(?P<year>[0-9]{2,4})

    # Formato ISO
    |(?P<isoyear>[0-9]{4})-(?P<isomonth>[0-9]{2})-(?P<isoday>[0-9]{2})
""", re.VERBOSE)


def parse(text: str) -> datetime.date | None:
    """
    Tenta extrair uma data do texto usando a regex definida acima. 
    
    Se a regex corresponder, ela extrai os grupos nomeados e os converte em
    inteiros.
    
    Se o ano tiver apenas dois dígitos, ele é convertido para um formato de
    quatro dígitos assumindo que seja do século 21 (por exemplo, "23" se torna
    "2023").
    """
    m = DATE_REGEX.fullmatch(text)
    if m is None:
        return None
    groups = {k.removeprefix("iso"): v for k, v in m.groupdict().items() if v is not None}
    if len(groups["year"]) == 2:
        groups["year"] = "20" + groups["year"]

    kwargs = {k: int(v) for k, v in groups.items()}
    try:
        return datetime.date(**kwargs)
    except ValueError:
        return None


if __name__ == "__main__":
    print("Digite datas no formato YYYY-MM-DD ou dd/mm/yyyy")
    while True:
        try:
            text = input("> ")
        except (EOFError, SystemExit):
            break

        date = parse(text)
        print(date or "<error>")