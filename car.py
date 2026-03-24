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
        self.melhor_distancia_alvo = 1000 # Regista a melhor tentativa

# Adicionamos 'pista_paredes' como argumento
    def mover(self, obstaculos, pista_paredes): 
        if not self.vivo: return
        self.tempo_vivo += 1

        # Pega nos obstáculos que estão a cair
        list_rects = [obs.parede_esq for obs in obstaculos] + [obs.parede_dir for obs in obstaculos]
        
        # A MAGIA AQUI: Adiciona as bordas da pista à visão do carro!
        list_rects.extend(pista_paredes) 
        
        self.sensor.atualizar(list_rects)
        self.decidir()

        # Descobre qual é a parede que se aproxima
        obs_alvo = next((obs for obs in obstaculos if obs.y < self.y), None)
        if obs_alvo:
            centro_buraco = obs_alvo.gap_x + (obs_alvo.largura_buraco / 2)
            dist_atual = abs(self.x - centro_buraco)
            if dist_atual < self.melhor_distancia_alvo:
                self.melhor_distancia_alvo = dist_atual

    def decidir(self):
        inputs = [1.0 - (s / self.sensor.max_dist) for s in self.sensor.leituras]
        out = self.cerebro.forward(inputs)

        # Aumentamos a agilidade física do carro
        velocidade_lateral = 7.0 

        # NOVA LÓGICA DE DECISÃO: Força a ação!
        # out[0] é a vontade de ir para a Esquerda, out[1] para a Direita.
        # Se a diferença entre as vontades for mínima, ele vai a direito.
        if abs(out[0] - out[1]) < 0.1:
            pass # Fica a direito
        elif out[0] > out[1]: 
            self.x -= velocidade_lateral # Vai para a Esquerda
        else: 
            self.x += velocidade_lateral # Vai para a Direita

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

    def calcular_fitness(self):
        # 1. Passar buracos é o prémio absoluto
        fit = self.buracos_passados * 10000
        
        # 2. ALINHAMENTO É TUDO (Multiplicado por 5 para esmagar o tempo de vida)
        # Agora o carro que tenta alinhar com o buraco ganha milhares de pontos a mais
        bonus_mira = (1000 - self.melhor_distancia_alvo) * 5
        if bonus_mira > 0:
            fit += bonus_mira

        # 3. Tempo de vida passou a ser apenas um desempate menor
        fit += self.tempo_vivo 

        if not self.vivo:
            # Punição reduzida (0.5 em vez de 0.1) para não destruir o fitness 
            # de quem foi corajoso e tentou virar rápido para o buraco!
            fit *= 0.5 
            
        return fit

    def desenhar(self, tela):
        cor = (0, 255, 0) if self.vivo else (150, 0, 0)
        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 10))
        if self.vivo:
            self.sensor.desenhar(tela)