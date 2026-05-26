class Aventureiro:
    def __init__(self, nome):
        self.nome = nome
        self.localizacao = (0, 0)
        self.pontuacao = 0  # Adiciona o atributo de pontuação
        self.tesouros_coletados = []

    def mover(self, nova_localizacao):
        self.localizacao = nova_localizacao

    def coletar_tesouro(self, tesouro):
        self.tesouros_coletados.append(tesouro)
        self.pontuacao += tesouro.valor  # Atualiza a pontuação ao coletar um tesouro
