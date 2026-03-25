import pygame
from car import Car
from obstaculo import Obstaculo
from pista import Pista
import genetic

# O GÉNESIS: Inicializamos o motor gráfico e criamos o nosso "universo"
pygame.init()
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Simulação de IA - Algoritmo Genético")
clock = pygame.time.Clock()

# Tipografia para os dados do painel de controlo
fonte = pygame.font.SysFont("Arial", 16, bold=True)
fonte_pequena = pygame.font.SysFont("Arial", 12)

# O BERÇÁRIO: Ponto de partida de todos os carros
X_INIT, Y_INIT = 400, 500

# A POPULAÇÃO: 40 "indivíduos" tentam a sorte a cada geração
POPULACAO = 40
carros = [Car(X_INIT, Y_INIT) for _ in range(POPULACAO)]

# O CÉNARIO: Onde a vida e a morte acontecem
pista_jogo = Pista()
obstaculos = []
spawn_timer = 0
geracao = 1
rodando = True

# A MEMÓRIA DO MUNDO: Guardamos a história do melhor de cada geração
# para desenhar a curva de aprendizado
historico_fitness = []
melhor_carro_global = carros[0]

def desenhar_dashboard(tela, geracao, vivos, carros, historico):
    # O PAINEL DE CONTROLO DO "CRIADOR" (HUD)
    
    # Procura o recordista atual desta sessão
    recorde = max([c.buracos_passados for c in carros])
    
    # Textos informativos no canto superior esquerdo
    textos = [
        fonte.render(f"Geração: {geracao} | Vivos: {len(vivos)}", True, (255, 255, 255)),
        fonte.render(f"Melhor da Sessão: {recorde} buracos", True, (100, 255, 100)),
        fonte_pequena.render("[S] Guardar Modelo | [L] Carregar Modelo", True, (200, 200, 200))
    ]
    for i, txt in enumerate(textos):
        tela.blit(txt, (10, 10 + (i * 25)))

    # DESENHANDO A EVOLUÇÃO (O Eletrocardiograma da IA)
    # Aqui criamos o gráfico que mostra se eles estão a ficar mais inteligentes
    g_x, g_y, g_largura, g_altura = 580, 10, 200, 80
    pygame.draw.rect(tela, (40, 40, 40), (g_x, g_y, g_largura, g_altura)) # Fundo do gráfico
    pygame.draw.rect(tela, (100, 100, 100), (g_x, g_y, g_largura, g_altura), 1) # Borda
    tela.blit(fonte_pequena.render("Curva de Aprendizado (Fitness)", True, (150, 150, 150)), (g_x + 5, g_y + 5))

    # Desenha a linha verde mágica que sobe à medida que eles aprendem!
    if len(historico) > 1:
        max_val = max(historico) if max(historico) > 0 else 1
        pontos = []
        passo_x = (g_largura - 10) / (len(historico) - 1)
        
        # Conecta os pontos de glória de cada geração passada
        for i, val in enumerate(historico):
            px = g_x + 5 + (i * passo_x)
            py = (g_y + g_altura - 5) - ((val / max_val) * (g_altura - 25))
            pontos.append((px, py))
            
        pygame.draw.lines(tela, (0, 255, 100), False, pontos, 2)


# --- O CICLO DA VIDA (Loop Principal do Jogo) ---
while rodando:
    # 1. Escutando o Deus da Simulação (Você!)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: rodando = False
        if ev.type == pygame.KEYDOWN:
            # INTERVENÇÃO DIVINA: Guardar e Carregar cérebros
            if ev.key == pygame.K_s: 
                melhor_carro_global.cerebro.salvar()
            if ev.key == pygame.K_l: 
                for c in carros:
                    c.cerebro.carregar()

    # 2. Limpar o quadro para o próximo frame
    tela.fill((25, 25, 25))
    pista_jogo.desenhar(tela)

    # 3. Fazendo cair o céu (Gerador de Paredes)
    spawn_timer += 1
    if spawn_timer > 110:
        obstaculos.append(Obstaculo(largura_tela=LARGURA))
        spawn_timer = 0

    # 4. A Física do Mundo: As paredes descem implacavelmente
    for obs in obstaculos[:]:
        obs.mover()
        obs.desenhar(tela)
        # Se a parede passou e ninguém morreu, desaparece no infinito
        if obs.y > ALTURA:
            obstaculos.remove(obs)

    # 5. A LUTA PELA SOBREVIVÊNCIA
    vivos = [c for c in carros if c.vivo]
    
    for c in carros:
        c.desenhar(tela) # Todos são desenhados (os vivos brilham, os mortos apagam-se)
        
        if c.vivo:
            # Os vivos abrem os olhos e movem-se
            c.mover(obstaculos, pista_jogo.paredes)
            
            # O OLHEIRO DA EVOLUÇÃO: Fica sempre atento para ver quem é o "Einstein" do grupo
            if c.calcular_fitness() > melhor_carro_global.calcular_fitness():
                melhor_carro_global = c

            # A COROAR OS VENCEDORES: Verificamos se alguém passou pelo buraco sãos e salvos
            rect_carro = pygame.Rect(c.x, c.y, 20, 10)
            for obs in obstaculos:
                if c.id not in obs.carros_passaram and rect_carro.colliderect(obs.checkpoint_rect):
                    c.buracos_passados += 1
                    obs.carros_passaram.add(c.id) # Marca com orgulho que este carro passou!

            # O TESTE DA MORTE: Bater na parede é o fim da linha
            c.colisao(obstaculos, pista_jogo.paredes)

    # 6. Exibir a UI por cima de tudo
    desenhar_dashboard(tela, geracao, vivos, carros, historico_fitness)

    # 7. O APOCALIPSE E O RENASCIMENTO
    # Se todos os carros morreram, a geração acaba.
    if not vivos:
        # Guarda a nota final do génio desta geração no histórico
        historico_fitness.append(melhor_carro_global.calcular_fitness())
        
        # Chama o Algoritmo Genético para cruzar os melhores e criar filhos novos
        carros = genetic.criar_nova_geracao(carros, X_INIT, Y_INIT)
        melhor_carro_global = carros[0] # Reinicia o olheiro
        
        # Limpa o cenário para a nova geração nascer em paz
        obstaculos.clear()
        spawn_timer = 0
        geracao += 1

    # Atualiza o ecrã
    pygame.display.flip()
    
    # Ritmo do universo: 60 frames por segundo
    clock.tick(60)

# Fim da simulação
pygame.quit()