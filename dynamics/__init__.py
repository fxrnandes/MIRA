"""
Pacote dynamics — simula a propagação de fogo e fumaça no ambiente.

Exporta o autômato celular responsável pela evolução temporal dos
incêndios e da dispersão de fumaça no grid.
"""
from dynamics.fire_automaton import FireAutomaton

__all__ = ["FireAutomaton"]
