from __future__ import annotations # Permite usar AFND como tipo de retorno dentro da própria classe
from collections import defaultdict
import collections.abc # Para checagem de tipo iterável

class AFND:
    """
    Representa um Autómato Finito Não-Determinístico (AFND),
    incluindo suporte para transições épsilon (ε).
    """
    # Constante para representar a transição épsilon.
    EPSILON = "&"

    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_finais=None):
        self.estados = estados or set()
        self.alfabeto = alfabeto or set()
        # A principal diferença: o valor de uma transição é um CONJUNTO de estados de destino.
        # defaultdict(lambda: defaultdict(set)) significa que se uma chave [estado][simbolo] não existir,
        # ela será criada com um conjunto vazio como valor padrão.
        self.transicoes = transicoes or defaultdict(lambda: defaultdict(set))
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais or set()

    def __str__(self):
        """Retorna uma representação em string do AFND para fácil visualização."""
        transicoes_str = ""
        # Ordena para uma saída consistente e legível
        for origem, transicao in sorted(self.transicoes.items()):
            for simbolo, destinos in sorted(transicao.items()):
                # Os destinos são um conjunto, então os ordenamos para exibição.
                destinos_ordenados = sorted(list(destinos))
                transicoes_str += f"           - d({origem}, {simbolo}) = {set(destinos_ordenados)}\n"

        return f"""
        (AFND)
         - Estados Q: {sorted(list(self.estados))}
         - Alfabeto E: {sorted(list(self.alfabeto))}
         - Estado Inicial q0: {self.estado_inicial}
         - Estados Finais F: {sorted(list(self.estados_finais))}
         - Transições d:
{transicoes_str}
        """

    def salvar_automato(self, filepath: str):
        """Salva o autómato num ficheiro de texto num formato compatível com AFND."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"TIPO:AFND\n")
            f.write(f"ESTADOS:{','.join(sorted(list(self.estados)))}\n")
            f.write(f"ALFABETO:{','.join(sorted(list(self.alfabeto)))}\n")
            f.write(f"INICIAL:{self.estado_inicial}\n")
            f.write(f"FINAIS:{','.join(sorted(list(self.estados_finais)))}\n")
            f.write("TRANSICOES:\n")
            for origin_state in sorted(list(self.estados)):
                if origin_state in self.transicoes:
                    for symbol, dest_states in sorted(self.transicoes[origin_state].items()):
                        # Junta múltiplos estados de destino com um ponto e vírgula.
                        if dest_states:
                            f.write(f"{origin_state},{symbol},{';'.join(sorted(list(dest_states)))}\n")
        print(f"✔ AFND salvo com sucesso em '{filepath}'")

    @classmethod
    def from_file(cls, filepath: str) -> AFND:
        """Cria uma instância de AFND a partir de um ficheiro (método de fábrica)."""
        afnd = cls()
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]

        parsing_transitions = False
        for line in lines:
            if line.startswith("TRANSICOES:"):
                parsing_transitions = True
                continue

            if not parsing_transitions:
                if ':' in line:
                    key, value = line.split(':', 1)
                    if key == "ESTADOS" and value: afnd.estados = set(value.split(','))
                    elif key == "ALFABETO" and value: afnd.alfabeto = set(value.split(','))
                    elif key == "INICIAL": afnd.estado_inicial = value
                    elif key == "FINAIS" and value: afnd.estados_finais = set(value.split(','))
            else:
                try:
                    # Usa split com maxsplit=2 para garantir que os destinos fiquem juntos
                    origin, symbol, dests_str = line.split(',', 2)
                    # Divide os estados de destino pelo ponto e vírgula
                    dest_states = set(dests_str.split(';'))
                    # Adiciona o conjunto de estados de destino à transição
                    afnd.transicoes[origin][symbol].update(dest_states)
                except ValueError:
                    print(f"Aviso: Linha de transição mal formatada ignorada: '{line}'")
        
        print(f"✔ AFND carregado com sucesso de '{filepath}'")
        return afnd

    def e_fecho(self, estados: set[str] | str) -> set[str]:
        """
        Calcula o épsilon-fecho para um estado ou um conjunto de estados.
        O épsilon-fecho de um conjunto de estados S é o conjunto de todos os estados
        alcançáveis a partir de qualquer estado em S, seguindo apenas transições épsilon (ε).
        """
        # Garante que a entrada seja um conjunto de estados
        if isinstance(estados, str):
            estados_set = {estados}
        elif isinstance(estados, collections.abc.Iterable):
            estados_set = set(estados)
        else:
            raise TypeError("A entrada para e_fecho deve ser um estado (str) ou um conjunto de estados.")

        fecho = set(estados_set)
        pilha = list(estados_set) # Pilha para processar os estados

        while pilha:
            estado_atual = pilha.pop()
            # Obtém os estados alcançáveis via transição épsilon
            destinos_epsilon = self.transicoes.get(estado_atual, {}).get(self.EPSILON, set())
            
            for destino in destinos_epsilon:
                if destino not in fecho:
                    fecho.add(destino)
                    pilha.append(destino)
        
        return fecho

    def aceita(self, cadeia: str) -> bool:
        """
        Simula a execução do AFND para determinar se a cadeia de entrada é aceite.
        """
        # Começa com o épsilon-fecho do estado inicial.
        estados_atuais = self.e_fecho({self.estado_inicial})

        # Processa cada símbolo da cadeia de entrada.
        for simbolo in cadeia:
            proximos_estados = set()
            # Para cada estado ativo atual, encontra os próximos estados com base no símbolo.
            for estado in estados_atuais:
                proximos_estados.update(self.transicoes.get(estado, {}).get(simbolo, set()))
            
            # O novo conjunto de estados ativos é o épsilon-fecho dos estados alcançados.
            estados_atuais = self.e_fecho(proximos_estados)

        # Após processar toda a cadeia, a cadeia é aceite se qualquer um dos
        # estados ativos atuais for um estado final.
        # A função `isdisjoint` retorna True se os dois conjuntos não tiverem elementos em comum.
        return not estados_atuais.isdisjoint(self.estados_finais)


class AFNDBuscaPadrao(AFND):
    """
    Classe especializada que É um AFND para busca de padrões.
    Esta classe herda de AFND e se autoconfigura no construtor para
    reconhecer qualquer texto que contenha o padrão especificado.
    """

    def __init__(self, padrao: str):
        if not padrao:
            raise ValueError("O padrão não pode ser vazio.")
        
        # Inicializa a classe base (AFND) para ter acesso a self.estados, etc.
        super().__init__()
        
        self.padrao = padrao
        self.tamanho_padrao = len(padrao)
        
        # O método de construção agora preenche os atributos do próprio objeto.
        self._construir_automato_de_padrao(padrao)

    def _construir_automato_de_padrao(self, padrao: str):
        """
        Método privado que configura os atributos do próprio objeto (self)
        para funcionar como um AFND de busca de padrão.

        A construção segue uma lógica padrão:
        - Cria um estado para cada caractere no padrão, mais um estado inicial e um final.
        - Cria uma transição de "sucesso" para cada caractere do padrão para o próximo estado.
        - O estado 0 é especial:
            - Para qualquer caractere, ele pode retornar a si mesmo (para "deslizar" pelo texto).
            - Se o caractere for o primeiro do padrão, ele também pode transitar para o estado 1,
              iniciando uma possível correspondência.
        """
        tamanho = len(padrao)
        print(f"Construindo AFND para o padrão '{padrao}'...")

        # Configura os atributos herdados de AFND
        self.estados = {str(i) for i in range(tamanho + 1)}
        self.alfabeto = set(padrao) # O alfabeto é apenas o dos caracteres do padrão
        self.estado_inicial = '0'
        self.estados_finais = {str(tamanho)}

        # 1. Transições de "sucesso" que seguem o padrão
        for i in range(tamanho):
            self.transicoes[str(i)][padrao[i]].add(str(i + 1))

        # 2. Transições do estado inicial para lidar com a busca no texto
        # Para qualquer caractere no alfabeto, o estado 0 pode sempre voltar para si mesmo.
        for char in self.alfabeto:
            self.transicoes['0'][char].add('0')
        
        # O que torna este autómato não-determinístico é que, ao ver o primeiro
        # caractere do padrão no estado 0, ele pode tanto ficar em 0 como ir para 1.
        # A transição para 1 já foi adicionada no primeiro loop, então o conjunto
        # de transições para d(0, padrao[0]) será {0, 1}.

        print("✔ AFND de busca de padrão construído.")

    def buscar(self, texto: str) -> list[int]:
        """
        Executa a busca por todas as ocorrências do padrão no texto, simulando o AFND.
        """
        indices_encontrados = []
        # Começamos com o conjunto de estados ativos sendo o e-fecho do estado inicial.
        # Como este AFND não usa transições épsilon, é apenas o próprio estado inicial.
        estados_atuais = self.e_fecho({self.estado_inicial})

        for i, simbolo in enumerate(texto):
            # Se o símbolo não pertence ao alfabeto do padrão, ele não pode fazer parte
            # de uma correspondência. Resetamos para o estado inicial.
            if simbolo not in self.alfabeto:
                estados_atuais = self.e_fecho({self.estado_inicial})
                continue

            proximos_estados = set()
            for estado in estados_atuais:
                # Calcula os próximos estados possíveis a partir dos estados atuais e do símbolo lido
                proximos_estados.update(self.transicoes.get(estado, {}).get(simbolo, set()))
            
            # O novo conjunto de estados ativos é o e-fecho dos estados alcançados
            estados_atuais = self.e_fecho(proximos_estados)

            # Verifica se algum dos estados ativos é um estado final
            if not self.estados_finais.isdisjoint(estados_atuais):
                # Se sim, encontramos uma correspondência!
                # O índice inicial da correspondência é a posição atual menos o tamanho do padrão mais um.
                indice_inicial = i - self.tamanho_padrao + 1
                indices_encontrados.append(indice_inicial)

        return indices_encontrados