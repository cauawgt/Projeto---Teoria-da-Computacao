# pyautomata/conversion.py

# Usa imports relativos para aceder a outras partes do mesmo pacote
from .afd import AFD
from .afnd import AFND

def _epsilon_closure(states: set, transitions: dict) -> frozenset:
    """Função auxiliar para calcular o fecho-épsilon de um conjunto de estados."""
    closure = set(states)
    stack = list(states)
    while stack:
        current_state = stack.pop()
        # Obtém os estados alcançáveis com transição épsilon (se existirem)
        epsilon_dests = transitions.get(current_state, {}).get('EPSILON', set())
        for dest in epsilon_dests:
            if dest not in closure:
                closure.add(dest)
                stack.append(dest)
    # Retorna um frozenset para que possa ser usado como chave de dicionário
    return frozenset(closure)

def _format_state_name(state_set: frozenset) -> str:
    """Função auxiliar para criar um nome de estado canónico a partir de um conjunto."""
    if not state_set: return "PHI" # Representa o estado de erro/vazio
    return '_'.join(sorted(list(state_set)))


def convert_afnd_to_afd(afnd: AFND) -> AFD:
    """
    Converte um AFND num AFD equivalente usando o algoritmo de construção de subconjuntos.
    """
    afd = AFD(alfabeto=afnd.alphabet)
    
    queue = []
    processed_states = {}

    # 1. O estado inicial do AFD é o fecho-épsilon do estado inicial do AFND
    initial_closure = _epsilon_closure({afnd.initial_state}, afnd.transitions)
    afd.estado_inicial = _format_state_name(initial_closure)
    
    queue.append(initial_closure)
    processed_states[initial_closure] = afd.estado_inicial
    afd.estados.add(afd.estado_inicial)

    # 2. Processa cada "macro-estado" na fila
    while queue:
        current_macro_state = queue.pop(0)
        current_afd_state_name = processed_states[current_macro_state]

        # 3. Verifica se este novo estado do AFD é final
        if not current_macro_state.isdisjoint(afnd.final_states):
            afd.estados_finais.add(current_afd_state_name)

        # 4. Para cada símbolo do alfabeto, calcula o próximo macro-estado
        for symbol in afd.alfabeto:
            next_states_nondeterministic = set()
            for afnd_state in current_macro_state:
                next_states_nondeterministic.update(afnd.transitions.get(afnd_state, {}).get(symbol, set()))
            
            next_macro_state = _epsilon_closure(next_states_nondeterministic, afnd.transitions)
            
            if next_macro_state not in processed_states:
                new_afd_state_name = _format_state_name(next_macro_state)
                processed_states[next_macro_state] = new_afd_state_name
                afd.estados.add(new_afd_state_name)
                queue.append(next_macro_state)
            
            # 5. Adiciona a transição ao AFD
            dest_afd_state_name = processed_states[next_macro_state]
            if current_afd_state_name not in afd.transicoes:
                afd.transicoes[current_afd_state_name] = {}
            afd.transicoes[current_afd_state_name][symbol] = dest_afd_state_name

    return afd