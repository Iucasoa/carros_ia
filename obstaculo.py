import pygame
import random

class Obstaculo:
    def __init__(self, largura_tela=800):
        # Configurações da Parede e do Buraco
        self.altura_parede = 20 # Espessura da parede
        self.largura_buraco = 100 # Largura do buraco (espaço para o carro passar)
        self.x = 0
        self.y = -self.altura_parede # Começa fora da tela (no teto)
        self.velocidade = 3.0
        
        # Define aleatoriamente onde o buraco vai estar
        # O buraco precisa de uma margem lateral (ex: 50px) para não colidir com as bordas da pista
        self.margem = 50 
        self.gap_x = random.randint(self.margem, largura_tela - self.margem - self.largura_buraco)
        
        # Define as duas partes da parede para colisão
        self.parede_esq = pygame.Rect(self.x, self.y, self.gap_x, self.altura_parede)
        
        comeco_parede_dir = self.gap_x + self.largura_buraco
        largura_parede_dir = largura_tela - comeco_parede_dir
        self.parede_dir = pygame.Rect(comeco_parede_dir, self.y, largura_parede_dir, self.altura_parede)

        # Flag para controle de recompensa (apenas na main.py)
        # Uma "linha de checkpoint" virtual no meio do buraco
        self.checkpoint_rect = pygame.Rect(self.gap_x, self.y, self.largura_buraco, self.altura_parede)
        
        # Lista para armazenar quais IDs de carros já validaram a recompensa para ESTA parede
        self.carros_passaram = set()

    def mover(self):
        # Move tudo para baixo
        self.y += self.velocidade
        
        # Atualiza a posição física dos retângulos de colisão
        self.parede_esq.y = self.y
        self.parede_dir.y = self.y
        self.checkpoint_rect.y = self.y # Atualiza o checkpoint

    def desenhar(self, tela):
        # Desenha as paredes em cinza
        cor_parede = (180, 180, 180)
        pygame.draw.rect(tela, cor_parede, self.parede_esq)
        pygame.draw.rect(tela, cor_parede, self.parede_dir)
        
        # Opcional: Desenhar o checkpoint em azul fraco para diagnóstico
        # pygame.draw.rect(tela, (0, 0, 100), self.checkpoint_rect, 1)
    