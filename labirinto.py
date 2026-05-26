import random
from tesouro import Tesouro

class Labirinto:
    def __init__(self, largura=10, altura=10, num_tesouros=5):
        self.largura = largura
        self.altura = altura
        self.inicio = (0, 0)
        self.estrutura, self.fim = self.gerar_labirinto()
        self.tesouros = self.gerar_tesouros(num_tesouros)
        self.perigos = []

    def gerar_labirinto(self):
        # Inicializa todas as células como paredes
        labirinto = [[1 for _ in range(self.largura)] for _ in range(self.altura)]
        trilha = []

        # Define a função de DFS
        def dfs(x, y):
            # Adiciona a posição atual à trilha
            trilha.append((x, y))
            # Define as direções de movimento
            direcoes = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(direcoes)  # Embaralha as direções para aleatoriedade

            for dx, dy in direcoes:
                nx, ny = x + dx, y + dy
                nnx, nny = x + 2 * dx, y + 2 * dy

                if 0 <= nnx < self.largura and 0 <= nny < self.altura and labirinto[nny][nnx] == 1:
                    labirinto[ny][nx] = 0  # Marca a célula intermediária como caminho
                    labirinto[nny][nnx] = 0  # Marca a célula final como caminho
                    dfs(nnx, nny)

        # Começa o DFS do ponto inicial
        labirinto[0][0] = 0
        dfs(0, 0)

        # Define o ponto final como o último ponto na trilha
        fim = trilha[-1]

        return labirinto, fim

    def gerar_tesouros(self, num_tesouros):
        tesouros = []
        while len(tesouros) < num_tesouros:
            x = random.randint(0, self.largura - 1)
            y = random.randint(0, self.altura - 1)
            if self.estrutura[y][x] == 0 and (x, y) != self.inicio and (x, y) != self.fim:
                tesouros.append(Tesouro("Tesouro", (x, y)))
        return tesouros

    def adicionar_tesouro(self, tesouro):
        self.tesouros.append(tesouro)

    def remover_tesouro(self, tesouro):
        self.tesouros.remove(tesouro)

    def adicionar_perigo(self, perigo):
        self.perigos.append(perigo)

    def remover_perigo(self, perigo):
        self.perigos.remove(perigo)
