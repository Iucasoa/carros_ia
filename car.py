import pygame
import math
import random
from neural_network import NeuralNetwork
from sensor import Sensor

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        # NOVA FÍSICA: Variável para guardar o "embalo" do carro
        self.vel_x = 0.0 
        
        self.tempo_vivo = 0
        self.angulo = -math.pi / 2
        self.vivo = True
        self.buracos_passados = 0
        self.id = random.randint(1000, 9999)
        self.cerebro = NeuralNetwork()
        self.sensor = Sensor(self)
        
        self.melhor_distancia_alvo = 1000 

    def mover(self, obstaculos, pista_paredes): 
        if not self.vivo: return
        self.tempo_vivo += 1

        list_rects = [obs.parede_esq for obs in obstaculos] + [obs.parede_dir for obs in obstaculos]
        list_rects.extend(pista_paredes) 
        
        self.sensor.atualizar(list_rects)
        self.decidir()

        obs_alvo = next((obs for obs in obstaculos if obs.y < self.y), None)
        if obs_alvo:
            centro_buraco = obs_alvo.gap_x + (obs_alvo.largura_buraco / 2)
            dist_atual = abs(self.x - centro_buraco)
            
            if dist_atual < self.melhor_distancia_alvo:
                self.melhor_distancia_alvo = dist_atual

    def decidir(self):
        inputs = [1.0 - (s / self.sensor.max_dist) for s in self.sensor.leituras]
        out = self.cerebro.forward(inputs)

        # A MATEMÁTICA DA INÉRCIA
        forca_motor = 1.5  # O quão rápido ele consegue acelerar para os lados
        atrito = 0.8       # Simula o atrito dos pneus (0.8 significa que ele retém 80% da velocidade a cada frame)

        if abs(out[0] - out[1]) < 0.1:
            pass 
        elif out[0] > out[1]: 
            self.vel_x -= forca_motor # Acelera para a Esquerda
        else: 
            self.vel_x += forca_motor # Acelera para a Direita

        # Aplica o atrito para suavizar o movimento e impedir que a velocidade seja infinita
        self.vel_x *= atrito 
        
        # O carro agora desliza com base na inércia
        self.x += self.vel_x 

        # Barreiras de segurança
        if self.x < 30: 
            self.x = 30
            self.vel_x = 0 # Se bater na parede lateral da tela, perde todo o embalo
        if self.x > 770: 
            self.x = 770
            self.vel_x = 0

    def colisao(self, obstaculos, pista_paredes):
        # HURTBOX APRIMORADA: Focada no centro do carro
        hitbox = pygame.Rect(self.x - 8, self.y - 3, 16, 6)
        
        for obs in obstaculos:
            if hitbox.colliderect(obs.parede_esq) or hitbox.colliderect(obs.parede_dir):
                self.vivo = False
                
        for parede in pista_paredes:
            if hitbox.colliderect(parede):
                self.vivo = False

    def calcular_fitness(self):
        fit = self.buracos_passados * 10000
        
        bonus_mira = (1000 - self.melhor_distancia_alvo) * 5
        if bonus_mira > 0:
            fit += bonus_mira

        fit += self.tempo_vivo 

        if not self.vivo:
            fit *= 0.5 
            
        return fit

    def desenhar(self, tela):
        cor = (0, 255, 0) if self.vivo else (150, 0, 0)
        
        rect_visual = pygame.Rect(self.x - 10, self.y - 5, 20, 10)
        pygame.draw.rect(tela, cor, rect_visual)
        
        if self.vivo:
            self.sensor.desenhar(tela)