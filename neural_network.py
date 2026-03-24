import random
import math

class NeuralNetwork:
    def __init__(self):
        # Pesos fortes o suficiente para tomarem decisões claras desde o frame 1
        self.pesos = [
            [random.uniform(-1.0, 1.0) for _ in range(7)], 
            [random.uniform(-1.0, 1.0) for _ in range(7)], 
            [random.uniform(-1.0, 1.0) for _ in range(7)]  
        ]

    def ativacao(self, x):
        # Tanh retorna entre -1 e 1. Zero significa indecisão.
        return math.tanh(x)

    def forward(self, inputs):
        outputs = []
        for neuronio in self.pesos:
            soma = 0 
            for i in range(len(inputs)):
                soma += inputs[i] * neuronio[i]
            outputs.append(self.ativacao(soma))
        return outputs

    def mutar(self):
        # Mutação agressiva (20% de chance) para forçar a descoberta do buraco rápido
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                if random.random() < 0.2: 
                    self.pesos[i][j] += random.uniform(-1.0, 1.0)

    def crossover(self, outro_pai):
        filho = NeuralNetwork()
        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):
                filho.pesos[i][j] = self.pesos[i][j] if random.random() < 0.5 else outro_pai.pesos[i][j]
        return filho