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
        
        # A memória do carro: guarda o momento em que ele esteve mais perto da salvação
        self.melhor_distancia_alvo = 1000 

    def mover(self, obstaculos, pista_paredes): 
        # Se já bateu, o cérebro desliga e ele não faz mais nada
        if not self.vivo: return
        self.tempo_vivo += 1

        # Reúne tudo o que é perigoso (as paredes que estão a cair)
        list_rects = [obs.parede_esq for obs in obstaculos] + [obs.parede_dir for obs in obstaculos]
        
        # Dá ao carro a "visão periférica" para ele perceber onde a pista acaba
        # e não ficar a raspar nas laterais do ecrã por distração.
        list_rects.extend(pista_paredes) 
        
        # Os "olhos" do carro analisam o ambiente e enviam a informação para o cérebro
        self.sensor.atualizar(list_rects)
        self.decidir()

        # O carro foca-se na ameaça mais imediata (a parede que está logo acima dele)
        obs_alvo = next((obs for obs in obstaculos if obs.y < self.y), None)
        if obs_alvo:
            centro_buraco = obs_alvo.gap_x + (obs_alvo.largura_buraco / 2)
            dist_atual = abs(self.x - centro_buraco)
            
            # Se ele conseguiu alinhar-se melhor do que antes, regista essa vitória pessoal
            if dist_atual < self.melhor_distancia_alvo:
                self.melhor_distancia_alvo = dist_atual

    def decidir(self):
        # Transforma a distância que o sensor vê num sinal de pânico (1.0 = perigo iminente)
        inputs = [1.0 - (s / self.sensor.max_dist) for s in self.sensor.leituras]
        
        # O cérebro processa o medo e decide para onde virar o volante
        out = self.cerebro.forward(inputs)

        # A agilidade física do carro para se desviar a tempo
        velocidade_lateral = 7.0 

        # Combate à preguiça: se a vontade de ir para os dois lados for quase igual, 
        # ele mantém a calma e vai a direito.
        if abs(out[0] - out[1]) < 0.1:
            pass 
        # Se o cérebro gritar "Esquerda!", ele desliza para a esquerda
        elif out[0] > out[1]: 
            self.x -= velocidade_lateral 
        # Caso contrário, desliza para a direita
        else: 
            self.x += velocidade_lateral 

        # Barreiras de segurança físicas para não fugir da simulação
        if self.x < 20: self.x = 20
        if self.x > 760: self.x = 760

    def colisao(self, obstaculos, pista_paredes):
        rect = pygame.Rect(self.x, self.y, 20, 10)
        
        # Verifica se foi esmagado pelas paredes que caem
        for obs in obstaculos:
            if rect.colliderect(obs.parede_esq) or rect.colliderect(obs.parede_dir):
                self.vivo = False
                
        # Verifica se bateu de frente com os limites laterais da pista
        for parede in pista_paredes:
            if rect.colliderect(parede):
                self.vivo = False

    def calcular_fitness(self):
        # AVALIAÇÃO DA VIDA DO CARRO (Quem merece passar os genes à próxima geração?)
        
        # 1. O Prémio Maior: Atravessar o buraco é o objetivo de vida deles
        fit = self.buracos_passados * 10000
        
        # 2. A Coragem de Tentar: Mesmo que morra, se morreu a tentar alinhar-se com 
        # o buraco, ganha imensos pontos de mérito. Isto evita que fiquem parados.
        bonus_mira = (1000 - self.melhor_distancia_alvo) * 5
        if bonus_mira > 0:
            fit += bonus_mira

        # 3. O Instinto de Sobrevivência: Viver mais tempo ajuda a desempatar
        fit += self.tempo_vivo 

        # A Morte: Se o carro bater, perde metade da sua nota.
        # É uma punição, mas não tira tudo a zeros, porque queremos perdoar os
        # erros daqueles que foram corajosos e tentaram desviar-se à última hora.
        if not self.vivo:
            fit *= 0.5 
            
        return fit

    def desenhar(self, tela):
        # Os vivos brilham a verde, os que falharam ficam a vermelho escuro
        cor = (0, 255, 0) if self.vivo else (150, 0, 0)
        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 10))
        
        # Só desenha os "olhos" a laser se o carro ainda estiver consciente
        if self.vivo:
            self.sensor.desenhar(tela)