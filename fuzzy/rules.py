"""Base de regras IF-THEN inspirada em manuais de evacuação de incêndio (NR-23)."""
from skfuzzy import control as ctrl


def build_rules(temperature, smoke, fire_dist, danger) -> list:
    """
    Retorna ~12 regras fuzzy cobrindo os principais cenários de risco.

    Lógica geral:
      - Temperatura alta OU fumaça alta OU fogo próximo → perigo alto
      - Condições moderadas combinadas → perigo médio
      - Ambiente fresco, pouca fumaça e fogo distante → perigo baixo
    """
    return [
        # Situações críticas
        ctrl.Rule(temperature["high"],                            danger["high"]),
        ctrl.Rule(smoke["high"],                                  danger["high"]),
        ctrl.Rule(fire_dist["low"],                               danger["high"]),
        ctrl.Rule(temperature["high"] & fire_dist["low"],         danger["high"]),
        ctrl.Rule(smoke["high"]       & fire_dist["low"],         danger["high"]),

        # Situações moderadas
        ctrl.Rule(temperature["medium"] & smoke["medium"],        danger["medium"]),
        ctrl.Rule(temperature["medium"] & fire_dist["medium"],    danger["medium"]),
        ctrl.Rule(smoke["medium"]       & fire_dist["medium"],    danger["medium"]),
        ctrl.Rule(temperature["low"]    & fire_dist["medium"],    danger["medium"]),

        # Situações seguras
        ctrl.Rule(temperature["low"] & smoke["low"] & fire_dist["high"], danger["low"]),
        ctrl.Rule(smoke["low"]       & fire_dist["high"],                danger["low"]),
        ctrl.Rule(temperature["low"] & fire_dist["high"],                danger["low"]),
    ]
