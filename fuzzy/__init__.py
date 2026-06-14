"""
Pacote fuzzy — sistema de inferência fuzzy para avaliação de perigo.

Exporta as variáveis linguísticas, a base de regras e o motor de
inferência Mamdani usado para calcular o nível de perigo de cada célula.
"""
from fuzzy.inference import FuzzyInferenceSystem

__all__ = ["FuzzyInferenceSystem"]
