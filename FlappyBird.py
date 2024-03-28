import pygame
import sys
import os
import random
from itens import Itens
from pygame.locals import *
import neat

pygame.init()

ai_jogando = True
geracao = 0

width, height = 500, 800
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo com Pássaro")

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', "pipe.png")))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', "base.png")))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', "bg.png")))
IMAGENS_PASSARO = [
    pygame.image.load(os.path.join('imgs', "bird1.png")),
    pygame.image.load(os.path.join('imgs', "bird2.png")),
    pygame.image.load(os.path.join('imgs', "bird3.png")),
]
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 40)

class Passaro(Itens):

    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, win, x, y, w, h, img, r):
        super().__init__(win, x, y, w, h, img, r)
        self.x = x
        self.y = y
        self.r = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.img = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1    
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.r < self.ROTACAO_MAXIMA:
                self.r = self.ROTACAO_MAXIMA
        else:
            if self.r > -90:
                self.r -= self.VELOCIDADE_ROTACAO        

    def desenhar(self):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.img = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.img = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.img = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.img = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.img = self.IMGS[0]
            self.contagem_imagem = 0

        if self.r <= -80:
            self.img = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2            
        self.mover()
        self.show()

class Cano(Itens):
    DISTANCIA = 200
    VELOCIDADE = 5          

    def __init__(self, win, x, y, w, h, img):
        super().__init__(win, x, y, w, h, img, 0)
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(img, False, True)
        self.CANO_BASE = img
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA
    
    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self):
        self.mover()
        self.win.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        self.win.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
     
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)              
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro.mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro.mask.overlap(base_mask, distancia_base)

        if (base_ponto or topo_ponto):
            return True
        else:
            return False


class Chao(Itens):

    VELOCIDADE = 5

    def __init__(self, win, x, y, w, h, img):
        super().__init__(win, x, y, w, h, img, 0)
        self.y = y
        self.w = w
        self.x1 = 0
        self.x2 = self.w
      

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.w < 0:
            self.x1 = self.x2 + self.w
        if self.x2 + self.w < 0:
            self.x2 = self.x1 + self.w    

    def desenhar(self):
        self.mover()
        self.win.blit(self.img, (self.x1, self.y))
        self.win.blit(self.img, (self.x2, self.y))       


def desenhar_tela(passaros, chao, canos, pontos, win):
    win.blit(IMAGEM_BACKGROUND, (0,0))        
    for passaro in passaros:
        passaro.desenhar()

    for cano in canos:
        cano.desenhar() 

    
    pygame.time.delay(15)

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255,255,255))
    win.blit(texto, (width - 10 - texto.get_width(), 10))

    if ai_jogando:
        texto = FONTE_PONTOS.render(f"Geração: {geracao}", 1, (255,255,255))
        win.blit(texto, (10, 10))        

    chao.desenhar()  
    pygame.display.update()

def main(genomas, config):
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        lista_genomas = []
        passaros = []

        for _, genoma in genomas:
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(win, 50, 350, 70, 70, IMAGENS_PASSARO[0], 0))
    else:
        passaros = [Passaro(win, 50, 350, 70, 70, IMAGENS_PASSARO[0], 0)]
    
    chao = Chao(win, 0, 730, width, IMAGEM_CHAO.get_height(), IMAGEM_CHAO)
    canos = [Cano(win, 700, 0, IMAGEM_CANO.get_width(), IMAGEM_CANO.get_height(), IMAGEM_CANO)]
    pontos = 0
  
    run = True
    while run:
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if not ai_jogando:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()
        indice_cano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            run = False
            break

        for i, passaro in enumerate(passaros):
            lista_genomas[i].fitness += 0.1
            output = redes[i].activate((passaro.y, 
                                        abs(passaro.y - canos[indice_cano].altura), 
                                        abs(passaro.y - canos[indice_cano].pos_base)))
            if output[0] > 0.5:
                print(output[0])
                passaro.pular() 

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)

                    if ai_jogando:
                        lista_genomas[i].fitness -= 1
                        lista_genomas.pop(i)
                        redes.pop(i)

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)            

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(win, 600, 0, IMAGEM_CANO.get_width(), IMAGEM_CANO.get_height(), IMAGEM_CANO))

            for genoma in lista_genomas:
                genoma.fitness += 5

        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.img.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

                if ai_jogando:
                    lista_genomas[i].fitness -= 1
                    lista_genomas.pop(i)
                    redes.pop(i)


        desenhar_tela(passaros, chao, canos, pontos, win)

    if not run:
        return
    pygame.quit()

def rodar(caminho_config):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, caminho_config)    

    populacao = neat.Population(config)

    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando: 
        populacao.run(main, 50)
    else:
        main(None, None)     

if __name__ == "__main__":
    caminho = os.path.dirname(__file__)
    caminho_config = os.path.join(caminho, 'config.txt')
    rodar(caminho_config)
    main()