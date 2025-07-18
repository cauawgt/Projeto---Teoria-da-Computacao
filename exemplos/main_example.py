from __future__ import annotations
import sys
import os

# Adiciona o diretório pai (a raiz do projeto) ao path do Python.
# Isto permite que o script encontre e importe o pacote 'pyautomata'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora podemos importar a nossa biblioteca de forma limpa
from automatos import AFDBuscaPadrao, AFNDBuscaPadrao


if __name__ == "__main__":
    # --- Definições Iniciais ---
    automato1 = AFDBuscaPadrao("ab")
    print(automato1)
    # --- Exemplo de uso ---
    texto = "Ola, este é um exemplo de texto com o padrão ab. ababsdksvbababba"
    resultados = automato1.buscar(texto)
    print("Resultados da busca:", resultados)
    automato1.salvar_automato("afd_exemplo.txt")
    
    automato2 = AFNDBuscaPadrao("ab")
    print(automato2)
    # --- Exemplo de uso ---
    texto2 = "Ola, este é um exemplo de texto com o padrão ab."
    resultados2 = automato2.buscar(texto2)
    print("Resultados da busca:", resultados2)
    automato2.salvar_automato("afnd_exemplo.txt")