"""Carrega cenários de arquivos JSON para o Grid."""
import json
from world.grid import Grid
from world.cell import CellType


def load_scenario(path: str) -> Grid:
    """
    Lê um arquivo JSON de cenário e retorna um Grid populado.

    O JSON deve ter os campos: width, height e grid (array 2D de inteiros
    mapeados para CellType: 0=WALL, 1=FREE, 2=FIRE, 3=SMOKE, 4=EXIT, 5=AGENT_START).
    """
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    grid = Grid(data["width"], data["height"])
    for y, row in enumerate(data["grid"]):
        for x, val in enumerate(row):
            grid.set_cell(x, y, CellType(val))
    return grid
