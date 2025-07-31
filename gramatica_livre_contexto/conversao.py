from automatos import AFD, AP
from gramatica_livre_contexto import GLC

def conversao_AFD_para_GLC(afd: AFD) -> GLC:
    """
    Realiza a conversão de um AFD para uma Gramática Regular
    """
    variaveis = set(afd.estados)
    terminais = set(afd.alfabeto)
    variavel_inicial = afd.estado_inicial
    regras = dict()

    for estado in afd.estados:
        regras[estado] = {}

    for estado_partida, transicoes in afd.transicoes.items():
        num_regra = 1
        for simbolo, estado_destino in transicoes.items():
            regras[estado_partida][num_regra] = [simbolo, estado_destino]
            num_regra += 1
    
    # Regra 2: R_i -> ε para cada estado de aceitação
    for estado_final in afd.estados_finais:
        # Garante que o número da regra seja único para o estado final
        num_regra = max(regras[estado_final].keys(), default=0) + 1
        regras[estado_final][num_regra] = ['ε']

    glc = GLC(variaveis, terminais, regras, variavel_inicial)
    return glc

def conversao_GLC_para_AP_iniciante(glc: GLC) -> AP:
    """
    Converte uma Gramática Livre-do-Contexto (GLC) em um Autômato com Pilha
    (AP) equivalente.
    """
    estados_do_ap = {'q_inicio', 'q_loop', 'q_aceita'}

    alfabeto_de_entrada = set()
    for terminal in glc.E:
        alfabeto_de_entrada.add(terminal)

    # A pilha poderá conter variáveis, terminais e um símbolo especial '$'.
    alfabeto_da_pilha = set()
    for variavel in glc.V:
        alfabeto_da_pilha.add(variavel)
    for terminal in glc.E:
        alfabeto_da_pilha.add(terminal)
    alfabeto_da_pilha.add('$') # Marcador de fundo da pilha

    estado_inicial_do_ap = 'q_inicio'
    estados_de_aceitacao_do_ap = {'q_aceita'}

    funcao_de_transicao = {}

    # Regra 1: A transição inicial
    # Do estado inicial, sem ler nada da entrada (ε) e com a pilha vazia (ε),
    # vamos para o estado de loop e colocamos a variável inicial da gramática
    # e o marcador '$' na pilha.
    simbolo_inicial_pilha = glc.S + '$'
    funcao_de_transicao[('q_inicio', 'ε', 'ε')] = {('q_loop', simbolo_inicial_pilha)}

    # Regra 2: Transições para as regras de produção da gramática
    # Para cada variável no topo da pilha, podemos substituí-la por uma de suas produções.
    for variavel in glc.R:
        producoes = glc.R[variavel]
        for producao in producoes:
            # A chave da nossa regra de transição
            chave_transicao = ('q_loop', 'ε', variavel)

            # Se ainda não criamos uma regra para esta chave, criamos um conjunto vazio
            if chave_transicao not in funcao_de_transicao:
                funcao_de_transicao[chave_transicao] = set()

            # A gramática deriva para a frente, mas a pilha funciona de trás para frente (LIFO).
            # Por isso, invertemos a produção antes de colocar na pilha.
            # Ex: Se a regra é A -> XY, desempilhamos A e empilhamos Y e depois X.
            producao_para_empilhar = ""
            if producao: # Se a produção não for vazia (ε)
                # Inverte a lista de símbolos e junta em uma string
                producao_invertida_lista = list(reversed(producao))
                producao_para_empilhar = "".join(producao_invertida_lista)
            else: # Se for uma produção para ε
                producao_para_empilhar = 'ε' # Não empilha nada

            # Adiciona a nova transição
            funcao_de_transicao[chave_transicao].add(('q_loop', producao_para_empilhar))

    # Regra 3: Transições para os terminais
    # Se o símbolo no topo da pilha for um terminal igual ao símbolo da entrada,
    # nós o consumimos (tiramos da pilha e avançamos na entrada).
    for terminal in glc.E:
        funcao_de_transicao[('q_loop', terminal, terminal)] = {('q_loop', 'ε')}

    # Regra 4: A transição final para aceitação
    # Se chegarmos ao final da entrada e a pilha contiver apenas o marcador '$',
    # significa que a palavra foi reconhecida. Vamos para o estado de aceitação.
    funcao_de_transicao[('q_loop', 'ε', '$')] = {('q_aceita', 'ε')}

    # 6. Criar e retornar o objeto do autômato com pilha
    automato_resultante = AP(
        Q=estados_do_ap,
        E=alfabeto_de_entrada,
        G=alfabeto_da_pilha,
        d=funcao_de_transicao,
        q0=estado_inicial_do_ap,
        F=estados_de_aceitacao_do_ap
    )

    return automato_resultante