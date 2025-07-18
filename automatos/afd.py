from __future__ import annotations # Permite usar AFD como tipo de retorno dentro da própria classe
from collections import defaultdict


class AFD:
    """
    Representa um Autómato Finito Determinístico (AFD).
    Esta classe é um contentor de dados genérico para um AFD.
    """

    def __init__(self, estados=None, alfabeto=None, transicoes=None, estado_inicial=None, estados_finais=None):
        self.estados = estados or set()
        self.alfabeto = alfabeto or set()
        self.transicoes = transicoes or defaultdict(dict)
        self.estado_inicial = estado_inicial
        self.estados_finais = estados_finais or set()

    def __str__(self):
        """Retorna uma representação em string do AFD para fácil visualização."""
        transicoes_str = ""
        # Ordena para uma saída consistente e legível
        for origem, transicao in sorted(self.transicoes.items()):
            for simbolo, destino in sorted(transicao.items()):
                transicoes_str += f"           - d({origem}, {simbolo}) = {destino}\n"

        return f"""
        (AFD)
         - Estados Q: {sorted(list(self.estados))}
         - Alfabeto E: {sorted(list(self.alfabeto))}
         - Estado Inicial q0: {self.estado_inicial}
         - Estados Finais F: {sorted(list(self.estados_finais))}
         - Transições d:
{transicoes_str}
        """

    def salvar_automato(self, filepath: str):
        """Salva o autómato num ficheiro de texto no formato especificado."""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"TIPO:AFD\n")
            f.write(f"ESTADOS:{','.join(sorted(list(self.estados)))}\n")
            f.write(f"ALFABETO:{','.join(sorted(list(self.alfabeto)))}\n")
            f.write(f"INICIAL:{self.estado_inicial}\n")
            f.write(f"FINAIS:{','.join(sorted(list(self.estados_finais)))}\n")
            f.write("TRANSICOES:\n")
            for origin_state in sorted(list(self.estados)):
                if origin_state in self.transicoes:
                    for symbol, dest_state in sorted(self.transicoes[origin_state].items()):
                        f.write(f"{origin_state},{symbol},{dest_state}\n")
        print(f"✔ AFD salvo com sucesso em '{filepath}'")

    @classmethod
    def from_file(cls, filepath: str) -> AFD:
        """Cria uma instância de AFD a partir de um ficheiro (método de fábrica)."""
        afd = cls()
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
                    if key == "ESTADOS" and value: afd.estados = set(value.split(','))
                    elif key == "ALFABETO" and value: afd.alfabeto = set(value.split(','))
                    elif key == "INICIAL": afd.estado_inicial = value
                    elif key == "FINAIS" and value: afd.estados_finais = set(value.split(','))
            else:
                try:
                    origin, symbol, dest = line.split(',')
                    afd.transicoes[origin][symbol] = dest
                except ValueError:
                    print(f"Aviso: Linha de transição mal formatada ignorada: '{line}'")
        
        print(f"✔ AFD carregado com sucesso de '{filepath}'")
        return afd


class AFDBuscaPadrao(AFD):
    """
    Classe especializada que É um AFD para busca de padrões.
    Esta classe herda de AFD e se autoconfigura no construtor.
    """

    def __init__(self, padrao: str):
        if not padrao:
            raise ValueError("O padrão não pode ser vazio.")
        
        # Inicializa a classe base (AFD) para ter acesso a self.estados, etc.
        super().__init__()
        
        self.padrao = padrao
        self.tamanho_padrao = len(padrao)
        
        # O método de construção agora preenche os atributos do próprio objeto.
        self._construir_automato_de_padrao(padrao)

    def _construir_automato_de_padrao(self, padrao: str):
        """
        Método privado que configura os atributos do próprio objeto (self)
        para funcionar como um AFD de busca de padrão.
        """
        tamanho_padrao = len(padrao)
        
        # Configura os atributos herdados de AFD
        self.estados = {str(i) for i in range(tamanho_padrao + 1)}
        self.estado_inicial = '0'
        self.estados_finais = {str(tamanho_padrao)}
        self.alfabeto = set(padrao)

        print(f"Construindo AFD para o padrão '{padrao}'...")
        for estado_atual_int in range(tamanho_padrao + 1):
            estado_atual_str = str(estado_atual_int)
            for caractere_lido in self.alfabeto:
                prefixo_do_padrao = padrao[:estado_atual_int]
                string_teste = prefixo_do_padrao + caractere_lido
                proximo_estado = 0
                tamanho_maximo_prefixo = min(tamanho_padrao, len(string_teste))

                for k in range(tamanho_maximo_prefixo, 0, -1):
                    prefixo_candidato = padrao[:k]
                    if string_teste.endswith(prefixo_candidato):
                        proximo_estado = k
                        break
                
                self.transicoes[estado_atual_str][caractere_lido] = str(proximo_estado)

        print("✔ AFD de busca de padrão construído.")

    def buscar(self, texto: str) -> list[int]:
        """
        Executa a busca pelo padrão no texto usando a lógica de simulação
        correta e robusta do AFD.
        """
        # Usa os atributos do próprio objeto (self)
        estado_atual = self.estado_inicial
        indices_encontrados = []

        for i, caractere_do_texto in enumerate(texto):
            # Obtém o próximo estado. O default é o estado inicial.
            estado_atual = self.transicoes.get(estado_atual, {}).get(
                caractere_do_texto, self.estado_inicial
            )

            if estado_atual in self.estados_finais:
                indice_inicial = i - self.tamanho_padrao + 1
                indices_encontrados.append(indice_inicial)

        return indices_encontrados