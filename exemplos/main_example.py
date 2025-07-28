from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automatos import AFD, AFDBuscaPadrao, AFNDBuscaPadrao, AFND


if __name__ == "__main__":
    # --- Definições Iniciais ---
    estados = {'1', '2', '3'}
    alfabeto = {'A', 'B'}
    estado_inicial = '1'
    estados_finais = {'2'}
    transicoes = {'1': {'A': '2', 'B': '1'},
                  '2': {'A': '2', 'B': '3'},
                  '3': {'A': '2', 'B': '1'}}
    automato1 = AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)
    print(automato1)
    print(automato1.aceita("1017"))
    
    print("="*40)
    automato2 = AFNDBuscaPadrao("AB")
    print(automato2)