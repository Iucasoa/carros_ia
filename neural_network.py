import random
import math

class NeuralNetwork:

    def__init__(self):
    
    self.pesos = [[random.uniform(-1,1) for _ in range(5)] for _ in range(3)]
    
    def ativacao(self, x):
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

        for i in range(len(self.pesos)):
            for j in range(len(self.pesos[i])):

                if random.random() < 0.1:
                    self.pesos[i][j] += random.uniform(-0.5,0.5)

    
