import random
from car import Car

def criar_nova_geracao(carros_antigos, x_inicial, y_inicial):
    # O DIA DO JULGAMENTO: Alinhamos todos os carros da geração que acabou de morrer, 
    # ordenando-os do melhor (o mais inteligente) para o pior (o mais azarado ou preguiçoso).
    carros_antigos.sort(key=lambda c: c.calcular_fitness(), reverse=True)
    
    tamanho_pop_original = len(carros_antigos)
    
    # O GRUPO REPRODUTOR: Apenas os 8 melhores carros da geração inteira 
    # terão o privilégio de ser os "pais" e "mães" da próxima geração.
    melhores = carros_antigos[:8] 
    novos_carros = []

    # A PROTEÇÃO DOS GÉNIOS (Elitismo): Pegamos nos 5 melhores absolutos e 
    # clonamo-los para o futuro sem mexer em nada. Isto é crucial! 
    # Garante que a sabedoria que eles conquistaram nunca se apaga por acidente, 
    # e que o gráfico de aprendizado nunca sofre quedas catastróficas.
    for i in range(5):
        elite = Car(x_inicial, y_inicial)
        elite.cerebro = melhores[i].cerebro
        novos_carros.append(elite)

    # A REPRODUÇÃO: Enquanto o "berçário" da nova geração não estiver cheio,
    # continuamos a criar novos filhos para substituir os carros que não eram bons.
    while len(novos_carros) < tamanho_pop_original:
        # Escolhemos dois pais aleatórios (mas lembre-se, apenas dentro daquele grupo de Elite)
        pai = random.choice(melhores)
        mae = random.choice(melhores)
        
        # O novo carro nasce no ponto de partida
        filho = Car(x_inicial, y_inicial)
        
        # HERANÇA E EVOLUÇÃO: O cérebro do filho é uma mistura das redes neurais 
        # do pai e da mãe (crossover).
        filho.cerebro = pai.cerebro.crossover(mae.cerebro)
        
        # Por fim, aplicamos a Mutação. É aquele pequeno "grão de loucura" ou 
        # criatividade que faz com que o filho possa tentar um caminho novo que os pais não viram.
        filho.cerebro.mutar()
        
        novos_carros.append(filho)
        
    # A nova geração está pronta para acordar e enfrentar a pista!
    return novos_carros