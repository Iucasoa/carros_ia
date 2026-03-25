import pygame
import random

class Obstaculo:
    def __init__(self, largura_tela=800):
        # A AMEAÇA E A SALVAÇÃO
        self.altura_parede = 25 # Espessura do bloco de cimento
        self.largura_buraco = 150 # O espaço por onde os carros escapam
        
        self.x = 0
        self.y = -self.altura_parede # Nasce escondida no topo do ecrã
        self.velocidade = 3.5 # A velocidade da queda implacável
        
        # Sorteia a posição do buraco, deixando uma margem de segurança nas bermas
        self.margem = 50 
        self.gap_x = random.randint(self.margem, largura_tela - self.margem - self.largura_buraco)
        
        # CONSTRUÇÃO CIVIL (As colisões físicas)
        self.parede_esq = pygame.Rect(self.x, self.y, self.gap_x, self.altura_parede)
        
        comeco_parede_dir = self.gap_x + self.largura_buraco
        largura_parede_dir = largura_tela - comeco_parede_dir
        self.parede_dir = pygame.Rect(comeco_parede_dir, self.y, largura_parede_dir, self.altura_parede)

        # O PORTAL INVISÍVEL (Onde a IA ganha os pontos)
        self.checkpoint_rect = pygame.Rect(self.gap_x, self.y, self.largura_buraco, self.altura_parede)
        
        # Memória para evitar que o mesmo carro ganhe pontos a dobrar nesta parede
        self.carros_passaram = set()

    def mover(self):
        # A GRAVIDADE: Desce os blocos de cimento e o portal a cada frame
        self.y += self.velocidade
        self.parede_esq.y = self.y
        self.parede_dir.y = self.y
        self.checkpoint_rect.y = self.y

    def desenhar(self, tela):
        # PINTURA DO CENÁRIO: Materializa as paredes no ecrã
        cor_parede = (180, 180, 180)
        pygame.draw.rect(tela, cor_parede, self.parede_esq)
        pygame.draw.rect(tela, cor_parede, self.parede_dir)