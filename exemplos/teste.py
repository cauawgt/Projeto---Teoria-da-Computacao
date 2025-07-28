from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gramatica_livre_contexto import GLC


if __name__ == "__main__":
    variaveis = {'A', 'B'}
    terminais = {'0', '1', '#'}
    varia_ini = 'A'
    regras = {'A': {1: '0A1', 2:'B'}, 
              'B': {1: '#'}}
    glc = GLC(variaveis, terminais, regras, varia_ini)

    print(glc)
    print(glc.derivar('0#10#1'))
