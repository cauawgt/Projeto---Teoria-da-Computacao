from collections import defaultdict

transicoes = defaultdict()

# o defaultdict é um dicionário,
# mas com um comportamento extra: quando você tenta acessar uma
# chave que ainda não existe, ele cria automaticamente um valor
# padrão para ela, ao invés de lançar um erro.

transicoes[0] = {'a': 1, 'b': 0}
transicoes[1] = {'a': 1, 'b': 2}
transicoes[2] = {'a': 1, 'b': 0}

estado_atual = 1

# print(transicoes.get(estado_atual, {}))

# Without defaultdict
t = {0: {'a': 1, 'b': 0},
     1: {'a': 1, 'b': 2},
     2: {'a': 1, 'b': 0}
     }

print(t.get(1, {}).get('b', -1))