from automatos import AFD, AP
from gramatica_livre_contexto import GLC

def conversao_AFD_para_GLC(afd: AFD) -> GLC:
    """
    Realiza a conversão de um AFD para uma Gramática Livre de Contexto (Regular)
    utilizando a estrutura de dados consistente.
    """
    variaveis = set(afd.estados)
    terminais = set(afd.alfabeto)
    variavel_inicial = afd.estado_inicial
    regras = dict()

    # Inicializa cada variável com uma LISTA vazia para suas produções
    for estado in afd.estados:
        regras[estado] = []

    # Regra 1: Para cada transição d(q_i, a) = q_j, adiciona a regra q_i -> a q_j
    for estado_partida, transicoes in afd.transicoes.items():
        for simbolo, estado_destino in transicoes.items():
            # Simplesmente adiciona a produção à lista
            regras[estado_partida].append([simbolo, estado_destino])
    
    # Regra 2: Para cada estado final q_f, adiciona a regra q_f -> ε
    for estado_final in afd.estados_finais:
        regras[estado_final].append(['ε'])

    # Cria a GLC com a estrutura de regras correta
    glc = GLC(
        V=variaveis, 
        E=terminais, 
        R=regras, 
        S=variavel_inicial
    )
    return glc

def conversao_GLC_para_AP(glc: GLC) -> AP:
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
    simbolo_inicial_pilha = glc.S + '$'
    funcao_de_transicao[('q_inicio', 'ε', 'ε')] = {('q_loop', simbolo_inicial_pilha)}

    # Regra 2: Transições para as regras de produção da gramática
    for variavel in glc.R:
        producoes = glc.R[variavel]
        for producao in producoes:
            
            chave_transicao = ('q_loop', 'ε', variavel)

            if chave_transicao not in funcao_de_transicao:
                funcao_de_transicao[chave_transicao] = set()

            producao_para_empilhar = ""
            if producao: 
                producao_invertida_lista = list(reversed(producao))
                producao_para_empilhar = "".join(producao_invertida_lista)
            else: 
                producao_para_empilhar = 'ε' 
            funcao_de_transicao[chave_transicao].add(('q_loop', producao_para_empilhar))

    # Regra 3: Transições para os terminais
    for terminal in glc.E:
        funcao_de_transicao[('q_loop', terminal, terminal)] = {('q_loop', 'ε')}

    funcao_de_transicao[('q_loop', 'ε', '$')] = {('q_aceita', 'ε')}

    
    automato_resultante = AP(
        Q=estados_do_ap,
        E=alfabeto_de_entrada,
        G=alfabeto_da_pilha,
        d=funcao_de_transicao,
        q0=estado_inicial_do_ap,
        F=estados_de_aceitacao_do_ap
    )

    return automato_resultante