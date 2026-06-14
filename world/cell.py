"""
Módulo responsável pela definição dos tipos de célula do ambiente 2D.

Cada célula do grid pode assumir um dos tipos definidos no enum CellType,
representando elementos estáticos (parede, saída) ou dinâmicos (fogo, fumaça).
"""
from enum import Enum


class CellType(Enum):
    """Enumeração dos possíveis tipos de célula no ambiente MIRA."""

    WALL = 0         # Parede — obstáculo intransponível
    FREE = 1         # Célula livre — transitável
    FIRE = 2         # Fogo — célula em chamas
    SMOKE = 3        # Fumaça — área com visibilidade reduzida
    EXIT = 4         # Saída — objetivo do agente
    AGENT_START = 5  # Posição inicial do agente
