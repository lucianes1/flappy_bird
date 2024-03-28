import pygame

class Itens:
    def __init__(self, win, x, y, w, h, img, r):
        # Inicialização direta dos atributos
        self.win = win
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self._img = img  # Usando _img para a imagem real
        self._r = r      # Usando _r para o ângulo real
        self.visible = True
        self.mask = None
        self.transformed_img = None
        self.update_transformations()

    # def __setattr__(self, name, value):
    #     permitted_attributes = ['win', 'x', 'y', 'w', 'h', '_img', '_r', 'visible', 
    #                             'mask', 'transformed_img', 'img', 'r', 
    #                             'vel_pulo', 'gravidade', 'pulando', 'vel_movimento']  # Adicione 'vel_movimento' aqui
    #     if name in permitted_attributes:
    #         super().__setattr__(name, value)
    #     else:
    #         raise AttributeError(f"Atributo '{name}' não é permitido na classe Itens.")

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, value):
        self._r = value
        self.update_transformations()

    # Métodos para img
    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        self._img = value
        self.update_transformations()   

    def update_transformations(self):
        if self._img is not None:
            self.transformed_img = pygame.transform.rotate(self.img, self.r)
            self.transformed_img = pygame.transform.scale(self.transformed_img, (self.w, self.h))
            self.mask = pygame.mask.from_surface(self.transformed_img)
        else:
            print("Aviso: Imagem não carregada corretamente.")
            
 
    def show(self):
        if self.visible:
            self.win.blit(self.transformed_img, (self.x, self.y))
