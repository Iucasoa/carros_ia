import random
import math

class NeuralNetwork:
    def __init__(self):
        # 7 sensores + 1 BIAS = 8 entradas. Apenas 2 saídas (Esquerda, Direita).
        self.pesos = [
            [random.uniform(-1.0, 1.0) for _ in range(8)], 
            [random.uniform(-1.0, 1.0) for _ in range(8)]
        ]

    def ativacao(self, x):
        return math.tanh(x)

    def forward(self, inputs):
        outputs = []
        for neuronio in self.pesos:
            soma = 0 
            for i in range(len(inputs)):
                soma += inputs[i] * neuronio[i]
            # Adiciona o BIAS (estímulo natural)
            soma += 1.0 * neuronio[-1]
            outputs.append(self.ativacao(soma))
        return outputs

    def mutar(self):
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                # Reduzido de 20% para 10% de probabilidade
                if random.random() < 0.10: 
                    # Reduzido de [-1.0, 1.0] para [-0.3, 0.3]. 
                    # Agora é um ajuste fino, não uma mudança radical!
                    self.pesos[i][j] += random.uniform(-0.3, 0.3)

    def crossover(self, outro_pai):
        filho = NeuralNetwork()
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                filho.pesos[i][j] = self.pesos[i][j] if random.random() < 0.5 else outro_pai.pesos[i][j]
        return filho