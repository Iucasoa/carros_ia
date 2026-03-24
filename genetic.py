import random
from car import Car

# Agora passamos os obstáculos para calcular quem estava mais alinhado
def criar_nova_geracao(carros_antigos, x_inicial, y_inicial, obstaculos):
    
    # Avalia o fitness passando a lista de obstáculos atual
    carros_antigos.sort(key=lambda c: c.calcular_fitness(obstaculos), reverse=True)
    
    melhores = carros_antigos[:5]
    novos_carros = []

    elite = Car(x_inicial, y_inicial)
    elite.cerebro = melhores[0].cerebro
    novos_carros.append(elite)

    while len(novos_carros) < 20:
        pai = random.choice(melhores)
        mae = random.choice(melhores)
        
        filho = Car(x_inicial, y_inicial)
        filho.cerebro = pai.cerebro.crossover(mae.cerebro)
        filho.cerebro.mutar()
        
        novos_carros.append(filho)
        
    return novos_carros