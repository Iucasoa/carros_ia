import pygame
from car import Car
from obstaculo import Obstaculo

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Carros com IA")

clock = pygame.time.Clock()

carros = []

import random

carros = []

for i in range(20):

    x = random.randint(200,600)
    y = random.randint(400,550)

    carros.append(Car(x,y))

obstaculos = []
spawn_timer = 0

rodando = True

while rodando:

    # eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    tela.fill((30,30,30))

    # gerar obstáculo
    spawn_timer += 1
    if spawn_timer > 60:
        obstaculos.append(Obstaculo())
        spawn_timer = 0

    # atualizar obstáculos
    for obstaculo in obstaculos:
        obstaculo.mover()
        obstaculo.desenhar(tela)

    # atualizar carros
    for carro in carros:

        if carro.vivo:

            carro.mover()
            carro.colisao(obstaculos)
            carro.desenhar(tela)

    pygame.display.update()

    clock.tick(60)

pygame.quit()