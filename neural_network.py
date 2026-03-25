import random
import math

class NeuralNetwork:
    def __init__(self):
        # O CÉREBRO (O DNA Inicial)
        # Quando um carro nasce, o seu cérebro é preenchido com ligações aleatórias.
        # Tem 7 recetores para os "olhos" (sensores) e 1 recetor extra para o "Instinto" (Bias).
        # Apenas 2 neurónios tomam a decisão final: um puxa o volante para a Esquerda, outro para a Direita.
        self.pesos = [
            [random.uniform(-1.0, 1.0) for _ in range(8)], 
            [random.uniform(-1.0, 1.0) for _ in range(8)]
        ]

    def ativacao(self, x):
        # O FILTRO DE EMOÇÕES (Tangente Hiperbólica)
        # Pega numa confusão de números matemáticos e esmaga-os numa decisão clara:
        # Retorna sempre um valor entre -1 (Odeio esta ideia!) e 1 (Quero muito fazer isto!).
        return math.tanh(x)

    def forward(self, inputs):
        # O RACIOCÍNIO (A magia acontece aqui)
        outputs = []
        for neuronio in self.pesos:
            soma = 0 
            # O cérebro analisa cada sinal de perigo que vem dos olhos e pondera
            # de acordo com o peso (a experiência) que dá a cada sensor.
            for i in range(len(inputs)):
                soma += inputs[i] * neuronio[i]
                
            # O INSTINTO NATURAL (Bias)
            # Mesmo que os olhos não vejam nada, o instinto dá um pequeno "empurrão" 
            # mental para que o carro não fique paralisado pelo medo ou pela dúvida.
            soma += 1.0 * neuronio[-1]
            
            # O neurónio finaliza o pensamento e grita a sua decisão
            outputs.append(self.ativacao(soma))
        return outputs

    def mutar(self):
        # O GRÃO DE LOUCURA (A Mutação Genética)
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                # 10% de probabilidade da natureza cometer um pequeno "erro" no DNA.
                # Sem estes pequenos erros, a espécie nunca teria ideias novas!
                if random.random() < 0.10: 
                    # Fazemos apenas uma pequena "massagem" no cérebro (-0.3 a 0.3).
                    # É um ajuste fino de personalidade, e não uma lavagem cerebral completa.
                    self.pesos[i][j] += random.uniform(-0.3, 0.3)

    def crossover(self, outro_pai):
        # A REPRODUÇÃO (O nascimento de um novo cérebro)
        filho = NeuralNetwork()
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                # Como num sorteio genético da vida real (50/50), o filho herda 
                # cada pedacinho de inteligência ou da mãe ou do pai.
                filho.pesos[i][j] = self.pesos[i][j] if random.random() < 0.5 else outro_pai.pesos[i][j]
        return filho