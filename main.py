import pygame
import random
# Lembre de manter suas importações certas conforme a estrutura das pastas
from car import Car
from obstaculo import Obstaculo # Obstaculo agora é uma Parede com Buraco
from pista import Pista
import genetic

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 18)

X_INIT, Y_INIT = 400, 550

# Inicialização da Geração 1
carros = [Car(X_INIT, Y_INIT) for _ in range(20)]
pista_jogo = Pista()
obstaculos = [] # Lista de Paredes com Buraco
spawn_timer = 0
geracao = 1
rodando = True

while rodando:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: rodando = False

    tela.fill((25, 25, 25))
    pista_jogo.desenhar(tela) # Bordas laterais

# Spawn de Paredes
    spawn_timer += 1
    
    # AUMENTADO: De 90/150 para 220. 
    # Agora o carro tem muito tempo para cruzar a tela de um lado pro outro!
    if spawn_timer > 220: 
        obstaculos.append(Obstaculo(largura_tela=800))
        spawn_timer = 0

    # Atualizar Obstáculos
    for obs in obstaculos[:]:
        obs.mover() # Agora a parede desce usando a velocidade dela
        obs.desenhar(tela)
        if obs.y > ALTURA:
            obstaculos.remove(obs)

    # Atualizar Carros Vivos
    vivos = [c for c in carros if c.vivo]
    for c in carros:
        c.desenhar(tela) # Desenha mortos e vivos (mortos em vermelho)
        
        if c.vivo:
            # 1. Movimento e Visão (Informa as Paredes para o sensor)
            c.mover(obstaculos)
            
            # 2. NOVO: Validação da Recompensa (Checkpoint)
            rect_carro_atual = pygame.Rect(c.x, c.y, 20, 10)
            
            for obs in obstaculos:
                # Se o ID deste carro ainda não Validou este buraco
                if c.id not in obs.carros_passaram:
                    # Se o carro colidiu com o checkpoint azul virtual do buraco
                    if rect_carro_atual.colliderect(obs.checkpoint_rect):
                        # RECOMPENSA VALIDADA!
                        c.buracos_passados += 1
                        obs.carros_passaram.add(c.id) # Marca este buraco como concluído por este ID
                        # Opcional: print para diagnóstico
                        # print(f"Carro {c.id} passou pelo buraco {geracao}! Total: {c.buracos_passados}")

            # 3. Colisão Física (Morte)
            # O c.colisao precisa checar parede esq, dir e bordas da pista
            c.colisao(obstaculos, pista_jogo.paredes)

    # Reinício da Geração (Evolução Gradual)
    if not vivos:
        print(f"Fim da Geração {geracao}. Evoluindo com foco em buracos passados.")
        # ATUALIZE ESTA LINHA: Passe os obstaculos como quarto parâmetro
        carros = genetic.criar_nova_geracao(carros, X_INIT, Y_INIT, obstaculos)
        obstaculos.clear()
        spawn_timer = 0
        geracao += 1

    # Texto na Tela
    info = fonte.render(f"Geração: {geracao} | Vivos: {len(vivos)}", True, (255, 255, 255))
    tela.blit(info, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()