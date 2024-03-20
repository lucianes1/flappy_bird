import pygame
import sys
import os
import random
from itens import Itens
from pygame.locals import *

# IMAGENS_PASSARO = [
#     pygame.image.load(os.path.join('imgs', "bird1.png")),
#     pygame.image.load(os.path.join('imgs', "bird2.png")),
#     pygame.image.load(os.path.join('imgs', "bird3.png"))

# ]

bird_img = pygame.image.load(os.path.join('imgs', "bird1.png"))
fundo_img = pygame.image.load(os.path.join('imgs', "fundo.png"))

pygame.init()
width, height = 500, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo com Pássaro")

class Passaro(Itens):
    def __init__(self, win, x, y, w, h, img):
        super().__init__(win, x, y, w, h, img, 0)
        self.vel_pulo = -10
        self.gravidade = 1
        self.pulando = False

    def pular(self):
        if self.pulando:
            self.y += self.vel_pulo
            self.vel_pulo += self.gravidade
            if self.y > 100:
                self.y = 100
                self.vel_pulo = -10
                self.pulando = False

    def desenhar(self):
        self.pular()
        self.show()           

class Fundo(Itens):
    def __init__(self, win, x, y, w, h, img):
        super().__init__(win, x, y, w, h, img, 0)
        self.vel_movimento = -1

    def mover(self):
        self.x += self.vel_movimento
        if self.x <= -self.w:
            self.x = self.w

    def desenhar(self):
        self.mover()
        self.show()        


def desenhar_tela(passaro, fundo, win):
    win.fill((255, 255, 255))  # Limpa a tela com uma cor de fundo
    fundo.desenhar()           # Desenha o fundo
    passaro.desenhar()         # Desenha o pássaro
    pygame.display.update()    # Atualiza a tela

def main():
    passaro = Passaro(win, 100, 100, 50, 50, bird_img)
    fundo = Fundo(win, 0, 0, width, height, fundo_img)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    passaro.pulando = True

        desenhar_tela(passaro, fundo, win)

    pygame.quit()

if __name__ == "__main__":
    main()