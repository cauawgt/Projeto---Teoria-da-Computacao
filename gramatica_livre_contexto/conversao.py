from automatos import AFD
from gramatica_livre_contexto import GLC

def conversao_AFD_para_GLC(afd: AFD) -> GLC:
    """
    Realiza a conversão de um Autômato Finito Determinístico (AFD) para
    uma Gramática Regular.
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
            # Regra: qi -> a qj
            regras[estado_partida][num_regra] = [simbolo, estado_destino]
            num_regra += 1

            # Regra de terminação: qi -> a (se qj for um estado final)
            if estado_destino in afd.estados_finais:
                regras[estado_partida][num_regra] = [simbolo]
                num_regra += 1


    glc = GLC(variaveis, terminais, regras, variavel_inicial)
    return glc