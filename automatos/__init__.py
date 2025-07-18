# automatos/__init__.py

"""
automatos: Uma biblioteca para manipulação de Autómatos Finitos.

Este pacote exporta as classes e funções essenciais para criar, manipular
e utilizar Autómatos Finitos Determinísticos (AFD) e Não-Determinísticos (AFND).
"""

# Expõe as classes principais para que possam ser importadas diretamente
from .afd import AFD
from .afd import AFDBuscaPadrao
from .afnd import AFND
from .afnd import AFNDBuscaPadrao

# Expõe os algoritmos e funções principais da biblioteca
from .conversao import convert_afnd_to_afd

__version__ = "1.0.0"

print("Pacote 'automatos' carregado.")