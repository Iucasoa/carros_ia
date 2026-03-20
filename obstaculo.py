import pygame
import random

class Obstaculo:

    def __init__(self):

        self.largura = 60
        self.altura = 20

        self.x = random.randint(100,700)
        self.y = -20

        self.velocidade = 3

    def mover(self):

        self.y += self.velocidade

    def desenhar(self, tela):

        pygame.draw.rect(tela,(200,200,200),(self.x,self.y,self.largura,self.altura))