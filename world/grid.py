"""Representa o ambiente 2D do edifício como uma grade de células."""
from world.cell import CellType


class Grid:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self._cells: list[list[CellType]] = [
            [CellType.FREE for _ in range(width)] for _ in range(height)
        ]

    def get_cell(self, x: int, y: int) -> CellType:
        return self._cells[y][x]

    def set_cell(self, x: int, y: int, cell_type: CellType) -> None:
        self._cells[y][x] = cell_type

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Retorna vizinhos válidos em 4-conectividade (cima/baixo/esquerda/direita)."""
        result = []
        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                result.append((nx, ny))
        return result

    def is_walkable(self, x: int, y: int) -> bool:
        """Célula é transitável se não for parede nem fogo."""
        return self.get_cell(x, y) not in (CellType.WALL, CellType.FIRE)
