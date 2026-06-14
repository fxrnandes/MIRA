# MIRA — Modelo Inteligente de Rota Autônoma

Sistema baseado em agente inteligente para evacuação autônoma de edifícios em situações de incêndio.
O agente navega em um ambiente 2D (grid) combinando **lógica fuzzy** — que avalia temperatura, densidade
de fumaça e proximidade do fogo — com **busca heurística A\*** sobre uma função de custo híbrida que
pondera distância ao objetivo e risco acumulado.

---

## Instalação

```bash
# 1. Crie e ative o ambiente virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# 2. Instale as dependências
pip install -r requirements.txt
```

---

## Como executar

```bash
# Configuração padrão — A* fuzzy com visualização pygame
python main.py --scenario scenarios/basic.json --algorithm astar_fuzzy --alpha 0.5

# A* puro (sem componente de risco fuzzy)
python main.py --scenario scenarios/basic.json --algorithm astar --alpha 0.0

# Greedy Best-First como baseline comparativo
python main.py --scenario scenarios/basic.json --algorithm greedy

# Sem visualização (modo headless para experimentos em lote)
python main.py --scenario scenarios/basic.json --algorithm astar_fuzzy --no-visualize

# Executar testes unitários
pytest tests/ -v
```

---

## Stack

| Tecnologia | Versão | Finalidade |
|-----------|--------|-----------|
| Python | 3.11+ | Linguagem principal |
| pygame | ≥ 2.5 | Visualização em tempo real |
| scikit-fuzzy | ≥ 0.4 | Sistema de inferência fuzzy (Mamdani) |
| numpy | ≥ 1.24 | Operações vetoriais e universos fuzzy |
| pytest | ≥ 7.0 | Testes unitários |

---

## Equipe

- Diego Planinscheck
- Gabriel Henrique Karing
- José Marcos Zoz Marques
- Vinicius Fernandes Carvalho
