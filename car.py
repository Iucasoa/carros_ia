import pygame
import math
import random
from neural_network import NeuralNetwork
from sensor import Sensor

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tempo_vivo = 0
        self.angulo = -math.pi / 2
        self.vivo = True
        self.buracos_passados = 0
        self.id = random.randint(1000, 9999)
        self.cerebro = NeuralNetwork()
        self.sensor = Sensor(self)

    def mover(self, obstaculos):
        if not self.vivo: return
        self.tempo_vivo += 1

        list_rects = [obs.parede_esq for obs in obstaculos] + [obs.parede_dir for obs in obstaculos]
        self.sensor.atualizar(list_rects)
        self.decidir()

    def decidir(self):
        # Inverte: 1.0 é parede grudada, 0.0 é caminho livre
        inputs = [1.0 - (s / self.sensor.max_dist) for s in self.sensor.leituras]
        out = self.cerebro.forward(inputs)

        velocidade_lateral = 7.5 

        # Como usamos Tanh, a saída vai de -1 a 1. 
        # Só agimos se a vontade for positiva (> 0.0)
        if out[0] > 0.0 and out[0] > out[1]: 
            self.x -= velocidade_lateral
        elif out[1] > 0.0 and out[1] > out[0]: 
            self.x += velocidade_lateral

        if self.x < 20: self.x = 20
        if self.x > 760: self.x = 760

    def colisao(self, obstaculos, pista_paredes):
        rect = pygame.Rect(self.x, self.y, 20, 10)
        for obs in obstaculos:
            if rect.colliderect(obs.parede_esq) or rect.colliderect(obs.parede_dir):
                self.vivo = False
        for parede in pista_paredes:
            if rect.colliderect(parede):
                self.vivo = False

    # A MAGIA ACONTECE AQUI: Recebemos os obstáculos para saber onde está o buraco
    def calcular_fitness(self, obstaculos):
        fit = (self.buracos_passados * 5000) + self.tempo_vivo

        # Bônus de Alinhamento: Premia quem morreu, mas morreu PERTO do buraco
        if obstaculos:
            # Pega o centro do buraco da primeira parede que está caindo
            centro_buraco = obstaculos[0].gap_x + (obstaculos[0].largura_buraco / 2)
            distancia_x = abs(self.x - centro_buraco)
            
            # Quanto menor a distância, maior o bônus (até 800 pontos extras)
            bonus_mira = 800 - distancia_x
            if bonus_mira > 0:
                fit += bonus_mira

        if not self.vivo:
            fit *= 0.3 
        return fit

    def desenhar(self, tela):
        cor = (0, 255, 0) if self.vivo else (150, 0, 0)
        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 10))
        if self.vivo:
            self.sensor.desenhar(tela)