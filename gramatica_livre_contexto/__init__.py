# Expõe as classes principais para que possam ser importadas diretamente
from .glc import GLC
from .conversao import conversao_AFD_para_GLC, conversao_GLC_para_AP


__version__ = "1.0.0"

print("Pacote 'gramatica_livre_contexto' carregado.")