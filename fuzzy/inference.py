"""Motor de inferência fuzzy Mamdani para avaliação de perigo de célula."""
from skfuzzy import control as ctrl
from fuzzy.variables import build_antecedents, build_consequent
from fuzzy.rules import build_rules


class FuzzyInferenceSystem:
    """Encapsula o pipeline fuzzy completo: fuzzificação → regras → defuzzificação."""

    def __init__(self) -> None:
        temp, smoke, fire_dist = build_antecedents()
        danger = build_consequent()
        rules = build_rules(temp, smoke, fire_dist, danger)

        system = ctrl.ControlSystem(rules)
        self._sim = ctrl.ControlSystemSimulation(system)

    def compute_danger(self, temp: float, smoke: float, fire_dist: float) -> float:
        """
        Calcula o índice de perigo (0-1) dado temperatura, fumaça e distância do fogo.

        Usa defuzzificação por centroide. Retorna 0.5 em caso de erro de inferência.
        """
        self._sim.input["temperature"] = max(0.0, min(100.0, temp))
        self._sim.input["smoke"]       = max(0.0, min(1.0,   smoke))
        self._sim.input["fire_dist"]   = max(0.0, min(20.0,  fire_dist))
        try:
            self._sim.compute()
            # Universo estendido para saturar nos extremos → clampa a [0, 1].
            return max(0.0, min(1.0, float(self._sim.output["danger"])))
        except Exception:
            return 0.5
