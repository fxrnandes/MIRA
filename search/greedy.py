"""
Greedy Best-First Search — expande sempre o nó com menor h(n).

Mais rápido que A* mas não garante otimalidade. Usado como baseline
comparativo nos experimentos do MIRA.
"""
import heapq
from collections.abc import Callable
from world.grid import Grid
from search.heuristics import manhattan


def greedy_best_first(
    start: tuple[int, int],
    goal: tuple[int, int],
    grid: Grid,
    heuristic: Callable | None = None,
) -> list[tuple[int, int]] | None:
    """Retorna o caminho de start até goal usando Greedy, ou None se não existir."""
    h = heuristic or manhattan
    open_set: list[tuple[float, tuple[int, int]]] = [(h(start, goal), start)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    visited: set[tuple[int, int]] = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in grid.neighbors(*current):
            if not grid.is_walkable(*neighbor) or neighbor in visited:
                continue
            came_from[neighbor] = current
            heapq.heappush(open_set, (h(neighbor, goal), neighbor))

    return None
