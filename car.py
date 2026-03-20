import pygame
import math

class Car:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.velocidade = 1
        self.angulo = -math.pi/2

        self.vivo = True

        self.sensores = []

    def mover(self):

        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade

        self.atualizar_sensores()

    def atualizar_sensores(self):

        self.sensores = []

        angulos = [-0.6, -0.3, 0, 0.3, 0.6]

        for a in angulos:

            angulo_sensor = self.angulo + a

            sensor_x = self.x + math.cos(angulo_sensor) * 100
            sensor_y = self.y + math.sin(angulo_sensor) * 100

            self.sensores.append((sensor_x, sensor_y))

    def desenhar(self, tela):

        if self.vivo:
            cor = (0,255,0)
        else:
            cor = (255,0,0)

        pygame.draw.rect(tela, cor, (self.x, self.y, 20, 10))

        for sensor in self.sensores:
            pygame.draw.line(tela,(255,0,0),(self.x,self.y),sensor,1)

    def colisao(self, obstaculos):

        carro_rect = pygame.Rect(self.x, self.y, 20, 10)

        for obstaculo in obstaculos:

            obst_rect = pygame.Rect(obstaculo.x, obstaculo.y, obstaculo.largura, obstaculo.altura)

            if carro_rect.colliderect(obst_rect):
                self.vivo = False