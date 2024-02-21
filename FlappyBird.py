import pygame
import os
import random
import itens
from pygame.locals import *

width, height = 800, 600
gover = True
cair = False
game = True

pygame.init()
win = pygame.display.set_mode((width, height))
bird0 = pygame.image.load("imgs/bird1.png")
bird1 = pygame.image.load("imgs/bird2.png")
bird2 = pygame.image.load("imgs/bird3.png")
piso = pygame.image.load("imgs/base.png")
tubo = pygame.image.load("imgs/pipe.png")
cena = pygame.image.load("imgs/bg.png")
asas = 0

ply = itens.Itens(win, 200, height / 2, 50, 50, bird0, 0)


def paint():
    global asas
    pygame.display.update()
    pygame.time.delay(10)
    win.fill(0x3C2EE)

    ply.show()

    asas += 1
    if asas < 10:
        ply.img = bird0
    elif asas < 15:
        ply.img = bird1
    else: 
        ply.img = bird2

    if asas > 20:
        asas = 0              

def control():
    global gover

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return False
    return True

while game:
    paint()
    game = control()



