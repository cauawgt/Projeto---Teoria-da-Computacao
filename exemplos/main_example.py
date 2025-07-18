from __future__ import annotations
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automatos import AFDBuscaPadrao


if __name__ == "__main__":
    # --- Definições Iniciais ---
    automato1 = AFDBuscaPadrao("ab")
    print(automato1)
    # --- Exemplo de uso ---
    texto = "Ola, este é um exemplo de texto com o padrão ab. ababsdksvbababba"
    resultados = automato1.buscar(texto)
    print("Resultados da busca:", resultados)
    automato1.salvar_automato("afd_exemplo.txt")
    