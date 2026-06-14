"""
Algoritmo A* com função de custo híbrida distância + risco fuzzy.

    g(n) = passos_acumulados + alpha * risco_fuzzy(n)
    f(n) = g(n) + manhattan(n, goal)
"""
import heapq
from collections.abc import Callable
from world.grid import Grid
from search.heuristics import manhattan


def astar(
    start: tuple[int, int],
    goal: tuple[int, int],
    grid: Grid,
    cost_fn: Callable[[tuple[int, int]], float],
    heuristic: Callable | None = None,
    alpha: float = 0.5,
) -> list[tuple[int, int]] | None:
    """
    Retorna o caminho de start até goal, ou None se não existir.

    cost_fn recebe uma posição e retorna o risco fuzzy (0-1) daquela célula.
    alpha = 0 → A* puro por distância; alpha = 1 → maximiza desvio de risco.
    """
    h = heuristic or manhattan
    open_set: list[tuple[float, tuple[int, int]]] = [(0.0, start)]
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g: dict[tuple[int, int], float] = {start: 0.0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in grid.neighbors(*current):
            if not grid.is_walkable(*neighbor):
                continue
            tentative_g = g[current] + 1.0 + alpha * cost_fn(neighbor)
            if tentative_g < g.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g[neighbor] = tentative_g
                heapq.heappush(open_set, (tentative_g + h(neighbor, goal), neighbor))

    return None
