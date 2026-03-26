# 🚗 Carros IA - Simulação de Condução Autônoma

[![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Pygame-ff69b4.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completo-brightgreen.svg)]()

## 📖 Descrição

Projeto de simulação computacional desenvolvido para demonstrar o aprendizado de máquina em agentes virtuais. O **Carros IA** é um ambiente onde veículos autônomos aprendem a desviar de obstáculos dinâmicos utilizando **Redes Neurais Artificiais** e **Algoritmos Genéticos**, programados 100% "do zero" (from scratch), sem o uso de bibliotecas de Machine Learning como TensorFlow ou PyTorch.

*(Sugestão: Adicione aqui um GIF animado demonstrando os carros se desviando dos obstáculos)*

## 🚀 Funcionalidades

O sistema simula um ecossistema evolutivo com os seguintes módulos:

### Módulo de Inteligência Artificial
- 🧠 Rede Neural Feedforward construída com matrizes nativas.
- ⚡ Função de ativação Tangente Hiperbólica (`Tanh`) para tomadas de decisão fluídas.
- 🎯 Implementação de neurônio de *Bias* (Instinto) para evitar paralisia decisional.

### Módulo de Algoritmo Genético
- 🧬 População dinâmica de 40 indivíduos simultâneos.
- 🏆 Sistema de *Reward Shaping* (Fitness) que recompensa alinhamento contínuo e pune colisões.
- 🔄 Operadores genéticos de *Crossover* (50/50) e Mutação controlada (10% de probabilidade, ajuste de ±0.3).
- 🛡️ Elitismo robusto que protege o DNA dos 5 melhores indivíduos (evitando o Esquecimento Catastrófico).

### Módulo Gráfico e Ferramentas
- 👁️ Sistema de visão por *Raycasting* otimizado.
- 📊 Dashboard analítico com renderização do gráfico de aprendizado em tempo real.
- 💾 Persistência de dados: *Save/Load* dos "cérebros" (pesos da rede) em formato JSON.

## 🛠️ Conceitos Matemáticos e Estruturais Aplicados

| Conceito | Descrição |
|----------|-----------|
| **Redes Neurais Artificiais** | Propagação de dados (*Forward Propagation*) multiplicando entradas (sensores) por pesos sinápticos. |
| **Algoritmos Genéticos** | Seleção natural, mutação paramétrica e recombinação genética para evolução de comportamento. |
| **Geometria Analítica** | Uso de trigonometria e cálculo de interseção de linhas (`clipline`) para o sistema de *Raycasting* e FOV. |
| **Serialização de Dados** | I/O de arquivos utilizando a biblioteca `json` para persistência das matrizes de aprendizado. |

## 💻 Tecnologias Utilizadas

- **Linguagem:** Python (3.x)
- **Motor Gráfico:** Pygame (2.x)
- **Matemática:** Bibliotecas nativas `math` e `random`
- **Persistência:** Biblioteca nativa `json`

## 📁 Estrutura do Projeto

```text
Carros-IA/
├── main.py              # Ponto de entrada, renderização do dashboard e loop principal
├── car.py               # Física do veículo, lógica de movimentação e cálculo de Fitness
├── neural_network.py    # Matemática do Forward Propagation, Crossover e Mutação
├── genetic.py           # Motor evolutivo, seleção de reprodutores e Elitismo
├── sensor.py            # Sistema de visão (Raycasting)
├── obstaculo.py         # Geração procedimental de terreno e alvos
├── pista.py             # Barreiras físicas e colisões do ambiente
└── README.md            # Documentação do projeto
```

## 🔧 Como Compilar e Executar

**1. Clone o repositório:**
```bash
git clone [https://github.com/Iucasoa/NOME_DO_SEU_REPOSITORIO.git](https://github.com/Iucasoa/NOME_DO_SEU_REPOSITORIO.git)
cd NOME_DO_SEU_REPOSITORIO
```

**2. Instale a dependência gráfica:**
```bash
pip install pygame
```

**3. Execute a simulação:**
```bash
python main.py
```

## 📝 Como Usar

1. Ao iniciar o `main.py`, a simulação começará automaticamente na Geração 1.
2. Acompanhe a evolução no Dashboard (Canto superior direito da tela).
3. Interações em tempo real (Atalhos de Teclado):
   - **`[S]` Guardar Modelo:** Exporta a inteligência do melhor carro para um arquivo `melhor_cerebro.json`.
   - **`[L]` Carregar Modelo:** Injeta a inteligência salva em toda a população atual.

## 📊 Exemplo de Saída (Dashboard)

```text
Geração: 32 | Vivos: 14
Melhor da Sessão: 5 buracos
[S] Guardar Modelo | [L] Carregar Modelo

+------------------------------------------+
| Curva de Aprendizado (Fitness)           |
|        /\                                |
|   /\  /  \    /\/\                       |
|  /  \/    \  /    \  /\                  |
| /          \/      \/  \                 |
+------------------------------------------+
```

## 👨‍💻 Autor

**João Lucas Oliveira de Andrade**
- GitHub: [@Iucasoa](https://github.com/Iucasoa)
- Formação: Estudante de Engenharia de Computação - UFERSA

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
