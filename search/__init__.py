"""
Pacote search — algoritmos de busca heurística para planejamento de rota.

Exporta as funções de busca A* e Greedy Best-First, bem como as
heurísticas utilizadas na avaliação de nós durante a exploração do espaço.
"""
from search.astar import astar
from search.greedy import greedy_best_first
from search.heuristics import manhattan, euclidean

__all__ = ["astar", "greedy_best_first", "manhattan", "euclidean"]
