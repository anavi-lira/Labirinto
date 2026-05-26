import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

from aventureiro import Aventureiro
from tesouro import Tesouro
from perigo import Perigo
from labirinto import Labirinto

class LabirintoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirinto Game")

        self.level = 1
        self.aventureiro = Aventureiro("Jogador1")
        self.labirinto = Labirinto()

        self.setup_ui()
        self.desenhar_labirinto()

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)

        self.level_up_pending = False

    def setup_ui(self):
        self.label = tk.Label(self.root, text=f"Level: {self.level}")
        self.label.pack()

        self.score_label = tk.Label(self.root, text=f"Pontuação: {self.aventureiro.pontuacao}")
        self.score_label.pack()

        self.next_level_button = tk.Button(self.root, text="Next Level", command=self.next_level)
        self.next_level_button.pack()

        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

    def desenhar_labirinto(self):
        self.canvas.delete("all")
        cell_size = 50
        for y, row in enumerate(self.labirinto.estrutura):
            for x, cell in enumerate(row):
                color = "white" if cell == 0 else "black"
                self.canvas.create_rectangle(
                    x * cell_size, y * cell_size,
                    (x + 1) * cell_size, (y + 1) * cell_size,
                    fill=color
                )
        inicio_x, inicio_y = self.labirinto.inicio
        self.canvas.create_rectangle(
            inicio_x * cell_size, inicio_y * cell_size,
            (inicio_x + 1) * cell_size, (inicio_y + 1) * cell_size,
            fill="blue"
        )
        fim_x, fim_y = self.labirinto.fim
        self.canvas.create_rectangle(
            fim_x * cell_size, fim_y * cell_size,
            (fim_x + 1) * cell_size, (fim_y + 1) * cell_size,
            fill="green"
        )
        for tesouro in self.labirinto.tesouros:
            tx, ty = tesouro.localizacao
            self.canvas.create_oval(
                tx * cell_size, ty * cell_size,
                (tx + 1) * cell_size, (ty + 1) * cell_size,
                fill="yellow"
            )
        av_x, av_y = self.aventureiro.localizacao
        self.aventureiro_oval = self.canvas.create_oval(
            av_x * cell_size, av_y * cell_size,
            (av_x + 1) * cell_size, (av_y + 1) * cell_size,
            fill="red"
        )

    def on_click(self, event):
        self.move_aventureiro(event.x, event.y)

    def on_drag(self, event):
        self.move_aventureiro(event.x, event.y)

    def move_aventureiro(self, x, y):
        cell_size = 50
        new_x = x // cell_size
        new_y = y // cell_size

        if 0 <= new_x < self.labirinto.largura and 0 <= new_y < self.labirinto.altura:
            if abs(new_x - self.aventureiro.localizacao[0]) + abs(new_y - self.aventureiro.localizacao[1]) == 1:
                if self.labirinto.estrutura[new_y][new_x] == 0:
                    self.aventureiro.mover((new_x, new_y))
                    self.coletar_tesouro((new_x, new_y))
                    self.desenhar_labirinto()
                    if (new_x, new_y) == self.labirinto.fim and not self.level_up_pending:
                        self.level_up_pending = True
                        self.root.after(4000, self.next_level)

    def coletar_tesouro(self, posicao):
        tesouro_a_coletar = None
        for tesouro in self.labirinto.tesouros:
            if tesouro.localizacao == posicao:
                tesouro_a_coletar = tesouro
                break
        if tesouro_a_coletar:
            tesouro_a_coletar.valor = 2 if self.level >= 10 else 1
            self.aventureiro.coletar_tesouro(tesouro_a_coletar)
            self.labirinto.remover_tesouro(tesouro_a_coletar)
            self.atualizar_pontuacao()

    def atualizar_pontuacao(self):
        self.score_label.config(text=f"Pontuação: {self.aventureiro.pontuacao}")

    def next_level(self):
        self.level += 1
        self.label.config(text=f"Level: {self.level}")
        self.labirinto = Labirinto()
        self.aventureiro.mover((0, 0))
        self.level_up_pending = False
        self.desenhar_labirinto()

        if self.level == 10:
            self.show_easter_egg()

    def show_easter_egg(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Easter Egg")

        self.canvas_egg = tk.Canvas(self.top, width=500, height=500)
        self.canvas_egg.pack()

        self.gif_path = "easter_egg.gif"
        self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(self.gif_path))]

        self.image_index = 0
        self.update_image()

    def update_image(self):
        self.canvas_egg.create_image(250, 250, image=self.sequence[self.image_index])
        self.image_index = (self.image_index + 1) % len(self.sequence)
        self.root.after(50, self.update_image)
