"""Define as variáveis linguísticas (antecedentes e consequente) do sistema fuzzy."""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def build_antecedents():
    """
    Cria as 3 variáveis de entrada com 3 termos linguísticos cada.

    - temperature : 0-100 °C  (low / medium / high)
    - smoke       : 0-1       (low / medium / high)
    - fire_dist   : 0-20 cél. (low / medium / high)  ← low = perto do fogo
    """
    temperature = ctrl.Antecedent(np.arange(0, 101, 1), "temperature")
    smoke = ctrl.Antecedent(np.arange(0, 1.01, 0.01), "smoke")
    fire_dist = ctrl.Antecedent(np.arange(0, 21, 1), "fire_dist")

    temperature["low"]    = fuzz.trimf(temperature.universe, [0,   0,  50])
    temperature["medium"] = fuzz.trimf(temperature.universe, [20, 50,  80])
    temperature["high"]   = fuzz.trimf(temperature.universe, [50, 100, 100])

    smoke["low"]    = fuzz.trimf(smoke.universe, [0,    0,   0.5])
    smoke["medium"] = fuzz.trimf(smoke.universe, [0.2,  0.5, 0.8])
    smoke["high"]   = fuzz.trimf(smoke.universe, [0.5,  1.0, 1.0])

    fire_dist["low"]    = fuzz.trimf(fire_dist.universe, [0,  0,  8])
    fire_dist["medium"] = fuzz.trimf(fire_dist.universe, [4, 10, 16])
    fire_dist["high"]   = fuzz.trimf(fire_dist.universe, [12, 20, 20])

    return temperature, smoke, fire_dist


def build_consequent():
    """
    Cria a variável de saída: danger (0-1) com 3 termos.

    O universo é estendido para [-0.3, 1.3] de propósito: com defuzzificação
    por centroide, triângulos confinados a [0,1] nunca produziriam saída
    próxima de 0% ou 100% (o centroide do termo extremo ficava preso em
    ~16,7% e ~83,3%). Estendendo os termos 'low' e 'high' para fora de [0,1],
    o centroide alcança os extremos; a saída é depois clampada a [0,1].
    """
    danger = ctrl.Consequent(np.arange(-0.3, 1.301, 0.01), "danger")
    danger["low"]    = fuzz.trimf(danger.universe, [-0.3, -0.3, 0.3])
    danger["medium"] = fuzz.trimf(danger.universe, [0.2,  0.5, 0.8])
    danger["high"]   = fuzz.trimf(danger.universe, [0.7,  1.3, 1.3])
    return danger
