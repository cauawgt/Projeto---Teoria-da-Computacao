class GLC:
    """
    Representa uma Gramática Livre-do-Contexto (GLC).

    Atributos:
        V (set): O conjunto de variáveis (símbolos não terminais).
        E (set): O conjunto de terminais (símbolos terminais).
        R (dict): Um dicionário com as regras de produção. As chaves são as 
                  variáveis e os valores são listas de strings representando 
                  as produções.
        S (str): A variável inicial.
    """

    def __init__(self, V=None, E=None, R=None, S=None):
        """Inicializa a Gramática Livre-do-Contexto."""
        self.V = V or set()
        self.E = E or set()
        self.R = R or dict()
        self.S = S

    def __str__(self):
        """Retorna uma representação em string da gramática."""
        regras_str = "" 
        if self.R:
            for variavel, producoes in self.R.items():
                
                producoes_formatadas = [
                    " ".join(p) for p in producoes.values()
                ]
                
                producoes_str = " | ".join(producoes_formatadas)
                regras_str += f"  {variavel} -> {producoes_str}\n"

        return (f"G = (V, E, R, S)\n\n"
                f"V = {self.V}\n"
                f"E = {self.E}\n"
                f"S = {self.S}\n\n"
                f"R (Regras de Produção):\n{regras_str}")

    def derivar(self, forma_setencial: str):
        """Executa um passo de derivação."""
        print(f"Analisando a setença: {forma_setencial}...")
        indices = []
        cadeia = []
        for i, l in enumerate(forma_setencial):
            cadeia.append(l)
            for v in self.V:
                if l == v:
                    indices.append(i)
        if not indices:
            print("Nenhuma variável encontrada para derivar.")
            return forma_setencial
        
        print(indices)

        indice_derivar = int(input("Escolha onde quer derivar: "))
        regra = int(input("Regra: "))
        variavel = cadeia[indice_derivar]
        cadeia[indice_derivar] = self.R[variavel][regra]

        result = ''
        for l in cadeia:
            result += l
        
        return result