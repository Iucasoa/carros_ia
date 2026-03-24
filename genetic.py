import random
from car import Car

def criar_nova_geracao(carros_antigos, x_inicial, y_inicial):
    carros_antigos.sort(key=lambda c: c.calcular_fitness(), reverse=True)
    
    tamanho_pop_original = len(carros_antigos)
    melhores = carros_antigos[:8] 
    novos_carros = []

    # AUMENTADO: Os 5 melhores carros passam para a próxima geração INTACTOS
    # Isso garante que a linha do gráfico NUNCA desce mais do que o recorde anterior
    for i in range(5):
        elite = Car(x_inicial, y_inicial)
        elite.cerebro = melhores[i].cerebro
        novos_carros.append(elite)

    while len(novos_carros) < tamanho_pop_original:
        pai = random.choice(melhores)
        mae = random.choice(melhores)
        
        filho = Car(x_inicial, y_inicial)
        filho.cerebro = pai.cerebro.crossover(mae.cerebro)
        filho.cerebro.mutar()
        
        novos_carros.append(filho)
        
    return novos_carros