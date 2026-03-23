import pygame
import math
from neural_network import NeuralNetwork

class Car:

    def __init__(self, x, y):

        self.distancia = 0
        self.ultimo_x = x

        self.cerebro = NeuralNetwork()
        self.tempo_vivo = 0

        self.x = x
        self.y = y

        self.velocidade = 1
        self.angulo = -math.pi / 2

        self.vivo = True

        self.sensores = []

    def mover(self, obstaculos):

        # calcular distância percorrida
        dist = abs(self.x - self.ultimo_x)
        self.distancia += dist
        self.ultimo_x = self.x

        self.tempo_vivo += 1

        self.decidir()

        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade

        self.atualizar_sensores(obstaculos)

    def atualizar_sensores(self, obstaculos):

        self.sensores = []

        angulos = [-0.6, -0.3, 0, 0.3, 0.6]
        max_dist = 120

        for a in angulos:

            angulo_sensor = self.angulo + a
            colidiu = False

            for d in range(max_dist):

                sensor_x = self.x + math.cos(angulo_sensor) * d
                sensor_y = self.y + math.sin(angulo_sensor) * d

                ponto = pygame.Rect(sensor_x, sensor_y, 2, 2)

                for obstaculo in obstaculos:

                    obst_rect = pygame.Rect(
                        obstaculo.x,
                        obstaculo.y,
                        obstaculo.largura,
                        obstaculo.altura
                    )

                    if ponto.colliderect(obst_rect):
                        self.sensores.append((sensor_x, sensor_y, d))
                        colidiu = True
                        break

                if colidiu:
                    break

            if not colidiu:
                self.sensores.append((sensor_x, sensor_y, max_dist))

    def desenhar(self, tela):

        cor = (0, 255, 0) if self.vivo else (255, 0, 0)

        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 10))

        for sensor in self.sensores:
            pygame.draw.line(
                tela,
                (255, 0, 0),
                (self.x, self.y),
                (sensor[0], sensor[1]),
                1
            )

    def colisao(self, obstaculos):

        carro_rect = pygame.Rect(self.x, self.y, 20, 10)

        for obstaculo in obstaculos:

            obst_rect = pygame.Rect(
                obstaculo.x,
                obstaculo.y,
                obstaculo.largura,
                obstaculo.altura
            )

            if carro_rect.colliderect(obst_rect):
                self.vivo = False

    def decidir(self):

        if len(self.sensores) < 5:
            return

        inputs = [s[2] / 120 for s in self.sensores]
        outputs = self.cerebro.forward(inputs)

        # decisões da IA
        if outputs[0] > 0.5:
            self.angulo -= 0.1

        if outputs[1] > 0.5:
            self.angulo += 0.1

        if outputs[2] > 0:
            self.velocidade = 2

    def calcular_fitness(self):

        if not self.vivo:
            return self.tempo_vivo + self.distancia

        return self.distancia + self.tempo_vivo