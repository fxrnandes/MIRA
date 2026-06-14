"""Funções heurísticas admissíveis para os algoritmos de busca."""
import math


def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Distância de Manhattan — admissível para movimentos em 4-conectividade."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: tuple[int, int], b: tuple[int, int]) -> float:
    """Distância Euclidiana — admissível quando diagonais são permitidas."""
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
