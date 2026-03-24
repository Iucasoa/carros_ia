import pygame
import math

class Sensor:
    def __init__(self, carro):
        self.carro = carro
        # Visão ainda mais longa (600 pixels) para reagir o mais cedo possível
        self.max_dist = 600 
        
        # AGORA SÃO 7 SENSORES! Um leque de -1.2 a 1.2 radianos
        self.angulos = [-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2]
        self.leituras = [self.max_dist] * 7 # 7 leituras iniciais

    def atualizar(self, lista_rects):
        self.leituras = []
        for a in self.angulos:
            angulo_sensor = self.carro.angulo + a
            dist_detectada = self.max_dist

            for d in range(0, self.max_dist, 5):
                sx = self.carro.x + math.cos(angulo_sensor) * d
                sy = self.carro.y + math.sin(angulo_sensor) * d
                
                colidiu = False
                for retangulo in lista_rects:
                    if retangulo.collidepoint(sx, sy):
                        dist_detectada = d
                        colidiu = True
                        break
                
                if colidiu:
                    break
                    
            self.leituras.append(dist_detectada)

    def desenhar(self, tela):
        for i, dist in enumerate(self.leituras):
            angulo_sensor = self.carro.angulo + self.angulos[i]
            dx = self.carro.x + math.cos(angulo_sensor) * dist
            dy = self.carro.y + math.sin(angulo_sensor) * dist
            pygame.draw.line(tela, (255, 0, 0), (self.carro.x, self.carro.y), (dx, dy), 1)