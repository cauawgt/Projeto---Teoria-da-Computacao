# pyautomata/afnd.py

from collections import defaultdict

class AFND:
    """
    Representa um Autómato Finito Não-Determinístico (AFND).

    A principal diferença para o AFD é que a função de transição
    mapeia para um CONJUNTO de estados de destino.
    """
    def __init__(self, states=None, alphabet=None, transitions=None, initial_state=None, final_states=None):
        self.states = states or set()
        self.alphabet = alphabet or set()
        # A função de transição retorna um conjunto de estados
        self.transitions = transitions or defaultdict(lambda: defaultdict(set))
        self.initial_state = initial_state
        self.final_states = final_states or set()
    
    def __str__(self):
        """Retorna uma representação em string do AFND."""
        transitions_str = ""
        for origin, trans in sorted(self.transitions.items()):
            for symbol, dests in sorted(trans.items()):
                if dests:
                    transitions_str += f"           - d({origin}, {symbol}) = {{{', '.join(sorted(list(dests)))}}}\n"
        return f"""
        (AFND)
         - Estados Q: {sorted(list(self.states))}
         - Alfabeto E: {sorted(list(self.alphabet))}
         - Estado Inicial q0: {self.initial_state}
         - Estados Finais F: {sorted(list(self.final_states))}
         - Transições d:
{transitions_str}
        """

def build_pattern_nfa(pattern: str, alphabet: set) -> AFND:
    """
    Constrói um AFND simples para busca de um padrão (pattern).
    A construção de um AFND para este fim é muito mais intuitiva do que a de um AFD.
    """
    m = len(pattern)
    states = {f'q{i}' for i in range(m + 1)}
    initial_state = 'q0'
    final_states = {f'q{m}'}
    
    afnd = AFND(states, alphabet, None, initial_state, final_states)
    
    # 1. Transições do "caminho principal" que reconhecem o padrão
    for i in range(m):
        char = pattern[i]
        origin_state = f'q{i}'
        dest_state = f'q{i+1}'
        afnd.transitions[origin_state][char].add(dest_state)

    # 2. Transições em q0 que permitem ao padrão começar em qualquer ponto do texto
    for char in alphabet:
        # q0 sempre tem uma transição para si mesmo para ignorar caracteres
        # que não iniciam o padrão. O não-determinismo entra em ação quando
        # o carácter é o primeiro do padrão, pois há duas transições possíveis.
        afnd.transitions['q0'][char].add('q0')
        
    return afnd