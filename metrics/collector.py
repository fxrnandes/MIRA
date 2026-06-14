"""Coleta métricas por episódio para comparação entre algoritmos."""
from dataclasses import dataclass


@dataclass
class EpisodeMetrics:
    algorithm: str
    scenario: str
    steps: int = 0
    accumulated_risk: float = 0.0
    replanning_count: int = 0
    nodes_expanded: int = 0
    execution_time: float = 0.0
    success: bool = False
    path_length: int = 0


class MetricsCollector:
    def __init__(self, algorithm: str, scenario: str) -> None:
        self.algorithm = algorithm
        self.scenario = scenario
        self._current = EpisodeMetrics(algorithm, scenario)
        self._history: list[EpisodeMetrics] = []

    def record_step(self, risk: float) -> None:
        self._current.steps += 1
        self._current.accumulated_risk += risk

    def record_replan(self) -> None:
        self._current.replanning_count += 1

    def record_nodes_expanded(self, count: int) -> None:
        self._current.nodes_expanded += count

    def record_execution_time(self, elapsed: float) -> None:
        self._current.execution_time += elapsed

    def finish_episode(self, success: bool, path_length: int) -> EpisodeMetrics:
        self._current.success = success
        self._current.path_length = path_length
        self._history.append(self._current)
        return self._current

    def generate_report(self) -> str:
        header = (
            f"{'Algoritmo':<14} {'Cenário':<10} {'Passos':>6} "
            f"{'Risco Acum.':>11} {'Replans':>7} {'Caminho':>7} {'Sucesso':>7}"
        )
        sep = "-" * len(header)
        lines = [header, sep]
        for m in self._history:
            lines.append(
                f"{m.algorithm:<14} {m.scenario:<10} {m.steps:>6} "
                f"{m.accumulated_risk:>11.3f} {m.replanning_count:>7} "
                f"{m.path_length:>7} {'Sim' if m.success else 'Não':>7}"
            )
        return "\n".join(lines)
