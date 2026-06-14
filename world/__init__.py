"""
Pacote world — define o ambiente 2D do MIRA.

Exporta as classes e funções principais para representação do ambiente:
Grid, CellType e load_scenario.
"""
from world.cell import CellType
from world.grid import Grid
from world.map_loader import load_scenario

__all__ = ["CellType", "Grid", "load_scenario"]
