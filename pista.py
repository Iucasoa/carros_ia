import pygame

class Pista:
    def __init__(self):
        self.paredes = []

        # Mantemos APENAS as bordas da tela para os carros não fugirem
        self.paredes.append(pygame.Rect(0, 0, 800, 20))   # Teto
        self.paredes.append(pygame.Rect(0, 580, 800, 20)) # Chão
        self.paredes.append(pygame.Rect(0, 0, 20, 600))   # Parede Esquerda
        self.paredes.append(pygame.Rect(780, 0, 20, 600)) # Parede Direita

    def desenhar(self, tela):
        for parede in self.paredes:
            pygame.draw.rect(tela, (200, 200, 200), parede)