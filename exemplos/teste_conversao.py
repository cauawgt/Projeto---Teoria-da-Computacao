from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gramatica_livre_contexto import GLC, conversao_AFD_para_GLC
from automatos import AFD

if __name__ == "__main__":

    estados = {'Q1', 'Q2', 'Q3'}
    alfabeto = {'A', 'B'}
    estado_inicial = 'Q1'
    estados_finais = {'Q2'}
    transicoes = {'Q1': {'A': 'Q2', 'B': 'Q1'},
                  'Q2': {'A': 'Q2', 'B': 'Q3'},
                  'Q3': {'A': 'Q2', 'B': 'Q1'}}
    automato1 = AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)
    print(automato1)

    glc1 = conversao_AFD_para_GLC(automato1)

    print(glc1)