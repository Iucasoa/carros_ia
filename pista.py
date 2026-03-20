import pygame

class Pista: 
    
    def __init__ (self, Largura, Altura):
    
        self.paredes = []
    
    # bordas da pista
    
        self.paredes.append(pygame.Rect(0,0,800,20))
        self.paredes.append(pygame.Rect(0,580,800,20))
        self.paredes.append(pygame.Rect(0,0,20,600))
        self.paredes.append(pygame.Rect(780,0,20,600))
    
    # obstáculos internoimport pygame

class Pista:

    def __init__(self):

        self.paredes = []

        # bordas da tela
        self.paredes.append(pygame.Rect(0,0,800,20))
        self.paredes.append(pygame.Rect(0,580,800,20))
        self.paredes.append(pygame.Rect(0,0,20,600))
        self.paredes.append(pygame.Rect(780,0,20,600))

        # obstáculos
        self.paredes.append(pygame.Rect(300,200,200,20))
        self.paredes.append(pygame.Rect(300,380,200,20))

    def desenhar(self, tela):

        for parede in self.paredes:
            pygame.draw.rect(tela,(200,200,200),parede)

        self.paredes.append(pygame.Rect(200,200,400,20))
        self.paredes.append(pygame.Rect(300,380,200,20))

    def desenhar(self, tela):

        for parede in self.paredes:
            pygame.draw.rect(tela,(200,200,200),parede)

