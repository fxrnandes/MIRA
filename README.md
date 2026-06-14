# MIRA — Modelo Inteligente de Rota Autônoma

Sistema baseado em agente inteligente para evacuação autônoma de edifícios em situações de incêndio.
O agente navega em um ambiente 2D (grid) combinando **lógica fuzzy** — que avalia temperatura, densidade
de fumaça e proximidade do fogo — com **busca heurística A\*** sobre uma função de custo híbrida que
pondera distância ao objetivo e risco acumulado.

---

## Arquitetura

| Módulo | Responsabilidade |
|--------|-----------------|
| `world/` | Definição do grid 2D, enum de tipos de célula (parede, fogo, saída) e carregamento de cenários JSON |
| `dynamics/` | Autômato celular para propagação estocástica do fogo e dispersão de fumaça |
| `fuzzy/` | Variáveis linguísticas, base de regras IF-THEN e motor de inferência Mamdani (scikit-fuzzy) |
| `search/` | Algoritmos A* com custo híbrido, Greedy Best-First e funções heurísticas admissíveis |
| `agent/` | Loop perceive-think-act com replanejamento dinâmico quando o ambiente muda |
| `visualization/` | Renderização pygame do grid em tempo real e overlay heatmap do risco fuzzy |
| `metrics/` | Coleta por episódio de passos, risco acumulado, replanejamentos e relatório comparativo |
| `scenarios/` | Mapas pré-definidos em JSON para os experimentos (basic, intermediate, complex) |
| `tests/` | Testes unitários por módulo com pytest |

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

## Status

> **Em desenvolvimento — Etapa 2 do trabalho**

A estrutura modular e os skeletons de classes estão definidos com docstrings,
type hints e assinaturas completas. A implementação dos algoritmos será
realizada na próxima etapa.

- [x] Estrutura de diretórios e pacotes
- [x] Skeletons com docstrings e type hints
- [x] Cenário básico JSON
- [x] Testes estruturados (pytest)
- [ ] Implementação do `world` (Grid, MapLoader)
- [ ] Implementação do `dynamics` (FireAutomaton)
- [ ] Implementação do `fuzzy` (variáveis, regras, inferência)
- [ ] Implementação do `search` (A*, Greedy, heurísticas)
- [ ] Implementação do `agent` (loop perceive-think-act)
- [ ] Implementação do `visualization` (Renderer, Heatmap)
- [ ] Implementação do `metrics` (Collector, Report)
- [ ] Experimentos comparativos

---

## Equipe

- Diego Planinscheck
- Gabriel Henrique Karing
- José Marcos Zoz Marques
- Vinicius Fernandes Carvalho
