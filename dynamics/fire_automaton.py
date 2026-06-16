"""Autômato celular para propagação de fogo e fumaça no grid."""
import random
from collections import deque
from world.grid import Grid
from world.cell import CellType


class FireAutomaton:
    def __init__(self, spread_prob: float = 0.3, smoke_range: int = 2) -> None:
        self.spread_prob = spread_prob
        self.smoke_range = smoke_range
        self._dist_cache: dict[tuple[int, int], int] = {}

    def step(self, grid: Grid) -> None:
        """Avança um passo: propaga fogo para vizinhos livres e fumaça ao redor."""
        new_fire = []
        new_smoke = []

        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_cell(x, y) != CellType.FIRE:
                    continue
                # Propaga fogo
                for nx, ny in grid.neighbors(x, y):
                    if grid.get_cell(nx, ny) == CellType.FREE:
                        if random.random() < self.spread_prob:
                            new_fire.append((nx, ny))
                # Propaga fumaça no raio configurado
                for dy in range(-self.smoke_range, self.smoke_range + 1):
                    for dx in range(-self.smoke_range, self.smoke_range + 1):
                        sx, sy = x + dx, y + dy
                        if 0 <= sx < grid.width and 0 <= sy < grid.height:
                            if grid.get_cell(sx, sy) == CellType.FREE:
                                new_smoke.append((sx, sy))

        for x, y in new_smoke:
            grid.set_cell(x, y, CellType.SMOKE)
        for x, y in new_fire:
            grid.set_cell(x, y, CellType.FIRE)

        self._dist_cache = {}  # invalida cache após mudança no grid

    # ------------------------------------------------------------------ #
    # Sensores — usados pelo Agent para alimentar o sistema fuzzy
    # ------------------------------------------------------------------ #

    def get_fire_distance(self, x: int, y: int, grid: Grid) -> float:
        """Distância em células até o foco de fogo mais próximo (BFS multi-origem)."""
        distances = self._get_all_distances(grid)
        return float(min(distances.get((x, y), 20), 20))

    def get_temperature(self, x: int, y: int, grid: Grid) -> float:
        """Temperatura estimada em °C: 100 no fogo, cai 10°C por célula de distância."""
        dist = self.get_fire_distance(x, y, grid)
        return max(0.0, 100.0 - dist * 10.0)

    def get_smoke_density(self, x: int, y: int, grid: Grid) -> float:
        """Densidade de fumaça normalizada (0-1) na célula."""
        ct = grid.get_cell(x, y)
        if ct == CellType.FIRE:
            return 1.0
        if ct == CellType.SMOKE:
            return 0.7
        for nx, ny in grid.neighbors(x, y):
            if grid.get_cell(nx, ny) in (CellType.FIRE, CellType.SMOKE):
                return 0.3
        return 0.0

    def _get_all_distances(self, grid: Grid) -> dict[tuple[int, int], int]:
        """BFS multi-origem a partir de todas as células em chamas."""
        if self._dist_cache:
            return self._dist_cache
        dist: dict[tuple[int, int], int] = {}
        queue: deque[tuple[int, int]] = deque()
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.get_cell(x, y) == CellType.FIRE:
                    dist[(x, y)] = 0
                    queue.append((x, y))
        while queue:
            x, y = queue.popleft()
            for nx, ny in grid.neighbors(x, y):
                # Paredes bloqueiam a propagação: o perigo não atravessa
                # uma parede, então células protegidas por ela ficam seguras.
                if (nx, ny) not in dist and grid.get_cell(nx, ny) != CellType.WALL:
                    dist[(nx, ny)] = dist[(x, y)] + 1
                    queue.append((nx, ny))
        self._dist_cache = dist
        return dist
