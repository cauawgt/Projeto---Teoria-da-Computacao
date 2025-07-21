from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from automatos import AFD, AFDBuscaPadrao, AFNDBuscaPadrao, AFND


if __name__ == "__main__":
    # --- Definições Iniciais ---
    estados = {'1', '2', '3'}
    alfabeto = {'0', '1'}
    estado_inicial = '1'
    estados_finais = {'2'}
    transicoes = {'1': {'0': '1', '1': '2'},
                  '2': {'1': '2', '0': '3'},
                  '3': {'0': '2', '1': '2'}}
    automato1 = AFD(estados, alfabeto, transicoes, estado_inicial, estados_finais)
    print(automato1)
    print(automato1.aceita("1017"))
    
    print("="*40)
    automato2 = AFNDBuscaPadrao("AB")
    print(automato2)