# 🚗 Carros IA - Simulação de Condução Autônoma

[![Linguagem](https://img.shields.io/badge/Linguagem-Python-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Pygame-ff69b4.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Completo-brightgreen.svg)]()

## 📖 Descrição

Projeto prático de simulação computacional construído 100% do zero. O **Carros IA** é um ambiente onde veículos autônomos aprendem a desviar de obstáculos dinâmicos. O projeto implementa Redes Neurais e Algoritmos Genéticos puramente através de matemática e lógica de programação, sem o uso de frameworks prontos (como TensorFlow).

## 🚀 Funcionalidades

O sistema simula um ecossistema de aprendizado de máquina dividido em três pilares:

### Inteligência Artificial (Rede Neural)
- 🧠 Rede Neural Feedforward com cálculos de matrizes nativos
- ⚡ Função de ativação Tangente Hiperbólica (`Tanh`)
- 🎯 Uso de *Bias* para forçar a tomada de decisão

### Algoritmo Genético
- 🧬 Gerenciamento de população (40 indivíduos por geração)
- 🏆 *Reward Shaping* (Cálculo de Fitness focado em alinhamento ao invés de apenas sobrevivência)
- 🛡️ Elitismo (Top 5 carros passam seus genes intactos) e Crossover (50/50)

### Interface e Ferramentas
- 👁️ Visão espacial otimizada por *Raycasting* (`clipline`)
- 📊 Dashboard analítico em tempo real com gráfico de aprendizado
- 💾 Persistência do modelo treinado em formato `.json`

## 🛠️ Conceitos Matemáticos Aplicados

| Conceito | Descrição |
|----------|-----------|
| **Matemática de Matrizes** | *Forward Propagation* multiplicando os inputs (sensores) pelos pesos (DNA) |
| **Geometria Analítica** | Cálculo de interseção de retas para simular o campo de visão dos sensores |
| **Evolução Computacional** | Seleção de reprodutores, mutação randômica e elitismo |
| **I/O de Arquivos** | Serialização e desserialização de dados com a biblioteca `json` |

## 💻 Tecnologias Utilizadas

- **Linguagem:** Python (3.x)
- **Renderização:** Pygame (2.x)
- **Módulos Nativos:** `math`, `random`, `json`

## 📋 Pré-requisitos

- **Python 3.x**
- **Git** para clonar o repositório
- Pacote **Pygame** instalado via `pip`

## 📁 Estrutura do Projeto

```text
Carros-IA/
├── main.py              # Ponto de entrada, dashboard e loop principal
├── car.py               # Física do veículo e cálculo de Fitness
├── neural_network.py    # Matemática da Rede Neural e Mutação
├── genetic.py           # Motor evolutivo e seleção
├── sensor.py            # Sistema de visão (Raycasting)
├── obstaculo.py         # Geração de terreno e alvos
└── pista.py             # Barreiras físicas do ambiente
```

## 🔧 Como Compilar e Executar

```bash
# Clone o repositório
git clone [https://github.com/Iucasoa/NOME_DO_SEU_REPOSITORIO.git](https://github.com/Iucasoa/NOME_DO_SEU_REPOSITORIO.git)
cd NOME_DO_SEU_REPOSITORIO

# Instale a dependência
pip install pygame

# Execute a simulação
python main.py
```

## 📝 Como Usar

```text
1. O simulador inicia automaticamente na Geração 1.
2. Acompanhe a evolução da IA pelo gráfico no canto superior direito.
3. Comandos de Teclado:
   - [S] Salvar Modelo: Salva o "cérebro" do melhor carro atual.
   - [L] Carregar Modelo: Injeta os pesos salvos em todos os carros vivos.
```

## 🎓 Aprendizados Principais

- Construção arquitetural de Machine Learning do zero
- Prevenção de problemas como *Reward Hacking* e *Catastrophic Forgetting*
- Otimização de processamento substituindo colisões de pixels por equações matemáticas
- Separação clara de responsabilidades (Lógica vs. Renderização)

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
+------------------------------------------+
```

## 🤝 Contribuindo

Este é um projeto de estudo contínuo. Sugestões são bem-vindas!

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/NovaAtivacao`)
3. Commit suas mudanças (`git commit -m 'Add nova função de ativação'`)
4. Push para a branch (`git push origin feature/NovaAtivacao`)
5. Abra um Pull Request

## 👨‍💻 Autor

**João Lucas Oliveira de Andrade**
- GitHub: [@Iucasoa](https://github.com/Iucasoa)
- Universidade: UFERSA (Engenharia de Computação)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
