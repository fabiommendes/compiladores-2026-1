type State = int
type Msg = str


class DFA:
    """
    Classe que representa um autômato finito determinístico (DFA).

    O DFA é definido por um estado inicial dado pela variável `initial`, 
    um conjunto de estados finais de aceite dado pela variável `final`, e um 
    dicionário de transições que mapeia um estado e uma mensagem para um novo estado.

    O método `accept` recebe um texto e valida se ele é aceito pelo autômato, ou seja,
    se a sequência de mensagens leva a um estado final de aceite.

    Use sub-classes para criar autômatos específicos, definindo os estados,
    mensagens e transições de acordo com a linguagem que deseja reconhecer.
    """
    initial: State = 0
    final: set[State] = {3, 4}
    transitions: dict[State, dict[Msg, State]] = {
        0: {
            "a": 1,
            "b": 2,
            "c": 2,
        },
        1: {
            "b": 3,
        },
        2: {
            "a": 4,
        },
    }


    def accept(self, text: str) -> bool:
        """
        Valida um texto segundo a linguagem definida pelo autômato.
        """
        state = self.initial

        for symbol in text:
            try:
                state = self.transitions[state][symbol]
            except KeyError:
                return False

        return state in self.final



# ==============================================================================
# Exemplo de uso do Autômato.
# ==============================================================================
if __name__ == "__main__":
    automaton = DFA()

    while True:
        try:
            text = input("> ")
        except (KeyboardInterrupt, EOFError):
            break

        if text == "":
            break
        elif automaton.accept(text):
            print("🎉🎉")
        else:
            print("💩")

