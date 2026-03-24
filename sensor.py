import pygame
import math

class Sensor:
    def __init__(self, carro):
        self.carro = carro
        self.max_dist = 600 
        self.angulos = [-1.2, -0.8, -0.4, 0, 0.4, 0.8, 1.2]
        self.leituras = [self.max_dist] * 7

    def atualizar(self, lista_rects):
        self.leituras = []
        for a in self.angulos:
            angulo_sensor = self.carro.angulo + a
            
            # Ponto de origem e ponto de destino do "raio" visual
            origem = (self.carro.x, self.carro.y)
            dx = self.carro.x + math.cos(angulo_sensor) * self.max_dist
            dy = self.carro.y + math.sin(angulo_sensor) * self.max_dist
            destino = (dx, dy)
            
            dist_detectada = self.max_dist
            
            # OTIMIZAÇÃO: Usa 'clipline' para cálculo instantâneo de interseção
            for retangulo in lista_rects:
                intersecao = retangulo.clipline(origem, destino)
                if intersecao:
                    # intersecao[0] é o ponto exato (x, y) onde a linha toca na parede
                    ponto_colisao_x, ponto_colisao_y = intersecao[0]
                    # Calcula a distância real usando o Teorema de Pitágoras
                    dist_real = math.hypot(ponto_colisao_x - self.carro.x, ponto_colisao_y - self.carro.y)
                    
                    if dist_real < dist_detectada:
                        dist_detectada = dist_real
                        
            self.leituras.append(dist_detectada)

    def desenhar(self, tela):
        for i, dist in enumerate(self.leituras):
            angulo_sensor = self.carro.angulo + self.angulos[i]
            dx = self.carro.x + math.cos(angulo_sensor) * dist
            dy = self.carro.y + math.sin(angulo_sensor) * dist
            # Linha desenhada apenas até onde detetou o objeto
            pygame.draw.line(tela, (255, 0, 0), (self.carro.x, self.carro.y), (dx, dy), 1)