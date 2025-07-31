class AP:
    """
    Representa um Autômato com Pilha.
    """

    def __init__(self, Q=None, E=None, G=None, d=None, q0=None, F=None):
        self.Q = Q or set()
        self.E = E or set()
        self.G = G or set()
        self.d = d or dict()
        self.q0 = q0
        self.F = F or set()

    def __str__(self):
        """Retorna uma representação em string do autômato com pilha."""
        transicoes_str = ""
        if self.d:
            for (estado_atual, simbolo_entrada, simbolo_pilha), transicoes in self.d.items():
                for (proximo_estado, push_simbolo) in transicoes:
                    transicoes_str += (f"  δ({estado_atual}, {simbolo_entrada}, {simbolo_pilha}) -> "
                                     f"({proximo_estado}, {push_simbolo})\n")

        return (f"AP = (Q, Σ, Γ, δ, q0, F)\n\n"
                f"Q = {self.Q}\n"
                f"Σ = {self.E}\n"
                f"Γ = {self.G}\n"
                f"q0 = {self.q0}\n"
                f"F = {self.F}\n\n"
                f"δ (Função de Transição):\n{transicoes_str}")