import pygame
from car import Car
from obstaculo import Obstaculo
from pista import Pista
import genetic

pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de IA - Algoritmo Genético")
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 16, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 12)

X_INIT, Y_INIT = 400, 500
POPULACAO = 40
carros = [Car(X_INIT, Y_INIT) for _ in range(POPULACAO)]
pista_jogo = Pista()
obstaculos = []
spawn_timer = 0
geracao = 1
rodando = True

# Variáveis Analíticas
historico_fitness = []
melhor_carro_global = carros[0]

def desenhar_dashboard(tela, geracao, vivos, carros, historico):
    # Textos do HUD
    recorde = max([c.buracos_passados for c in carros])
    textos = [
        fonte.render(f"Geração: {geracao} | Vivos: {len(vivos)}", True, (255, 255, 255)),
        fonte.render(f"Melhor da Sessão: {recorde} buracos", True, (100, 255, 100)),
        fonte_pequena.render("[S] Guardar Modelo | [L] Carregar Modelo", True, (200, 200, 200))
    ]
    for i, txt in enumerate(textos):
        tela.blit(txt, (10, 10 + (i * 25)))

    # Gráfico de Evolução
    g_x, g_y, g_largura, g_altura = 580, 10, 200, 80
    pygame.draw.rect(tela, (40, 40, 40), (g_x, g_y, g_largura, g_altura))
    pygame.draw.rect(tela, (100, 100, 100), (g_x, g_y, g_largura, g_altura), 1)
    tela.blit(fonte_pequena.render("Curva de Aprendizado (Fitness)", True, (150, 150, 150)), (g_x + 5, g_y + 5))

    if len(historico) > 1:
        max_val = max(historico) if max(historico) > 0 else 1
        pontos = []
        passo_x = (g_largura - 10) / (len(historico) - 1)
        for i, val in enumerate(historico):
            px = g_x + 5 + (i * passo_x)
            py = (g_y + g_altura - 5) - ((val / max_val) * (g_altura - 25))
            pontos.append((px, py))
        pygame.draw.lines(tela, (0, 255, 100), False, pontos, 2)

while rodando:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: rodando = False
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_s: # GUARDA O MODELO
                melhor_carro_global.cerebro.salvar()
            if ev.key == pygame.K_l: # CARREGA O MODELO
                for c in carros:
                    c.cerebro.carregar()

    tela.fill((25, 25, 25))
    pista_jogo.desenhar(tela)

    spawn_timer += 1
    if spawn_timer > 110:
        obstaculos.append(Obstaculo(largura_tela=LARGURA))
        spawn_timer = 0

    for obs in obstaculos[:]:
        obs.mover()
        obs.desenhar(tela)
        if obs.y > ALTURA:
            obstaculos.remove(obs)

    vivos = [c for c in carros if c.vivo]
    for c in carros:
        c.desenhar(tela)
        if c.vivo:
            # Passa as paredes da pista para que os sensores as vejam!
            c.mover(obstaculos, pista_jogo.paredes)
            
            # Avaliação em tempo real
            if c.calcular_fitness() > melhor_carro_global.calcular_fitness():
                melhor_carro_global = c

            rect_carro = pygame.Rect(c.x, c.y, 20, 10)
            for obs in obstaculos:
                if c.id not in obs.carros_passaram and rect_carro.colliderect(obs.checkpoint_rect):
                    c.buracos_passados += 1
                    obs.carros_passaram.add(c.id)

            c.colisao(obstaculos, pista_jogo.paredes)

    desenhar_dashboard(tela, geracao, vivos, carros, historico_fitness)

    if not vivos:
        historico_fitness.append(melhor_carro_global.calcular_fitness())
        carros = genetic.criar_nova_geracao(carros, X_INIT, Y_INIT)
        melhor_carro_global = carros[0]
        obstaculos.clear()
        spawn_timer = 0
        geracao += 1

    pygame.display.flip()
    clock.tick(60)

pygame.quit()