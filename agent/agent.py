"""
Agente inteligente de evacuação — loop perceive → decide → act.

O agente mantém um plano de caminho e o replaneja automaticamente quando
o fogo bloqueia o próximo passo. Se não houver caminho, usa fallback
(espera ou desce pelo vizinho de menor perigo).
"""
from world.grid import Grid
from world.cell import CellType
from dynamics.fire_automaton import FireAutomaton
from fuzzy.inference import FuzzyInferenceSystem
from metrics.collector import MetricsCollector
from search.astar import astar
from search.greedy import greedy_best_first


class Agent:
    def __init__(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
        grid: Grid,
        fire: FireAutomaton,
        fuzzy: FuzzyInferenceSystem,
        collector: MetricsCollector,
        algorithm: str = "astar_fuzzy",
        alpha: float = 0.5,
    ) -> None:
        self.position = start
        self.goal = goal
        self.grid = grid
        self.fire = fire
        self.fuzzy = fuzzy
        self.collector = collector
        self.algorithm = algorithm
        self.alpha = alpha
        self.plan: list[tuple[int, int]] = []
        # True quando não há rota até a saída — agente aguardando resgate.
        self.awaiting_rescue: bool = False

    # ------------------------------------------------------------------ #
    # Loop principal
    # ------------------------------------------------------------------ #

    def perceive(self) -> dict[str, float]:
        """Lê temperatura, fumaça e distância do fogo na posição atual."""
        x, y = self.position
        return {
            "temperature": self.fire.get_temperature(x, y, self.grid),
            "smoke":       self.fire.get_smoke_density(x, y, self.grid),
            "fire_dist":   self.fire.get_fire_distance(x, y, self.grid),
        }

    def decide(self) -> tuple[int, int] | None:
        """
        Retorna a próxima posição do plano.

        - Invalida o plano se o próximo passo estiver bloqueado (fogo/parede).
        - Recalcula o plano se estiver vazio.
        - Usa fallback se não houver caminho.
        """
        if self.position == self.goal:
            return None

        # Invalida se próximo passo está bloqueado
        if self.plan and not self.grid.is_walkable(*self.plan[0]):
            self.plan = []
            self.collector.record_replan()

        # Calcula plano se vazio
        if not self.plan:
            path = self._find_path()
            self.plan = path[1:] if path else []

        if self.plan:
            self.awaiting_rescue = False
            return self.plan.pop(0)

        # Sem rota até a saída — recorre ao fallback e sinaliza espera por resgate.
        self.awaiting_rescue = True
        return self.fallback_move()

    def act(self, next_pos: tuple[int, int] | None) -> None:
        """Move o agente e registra o risco da célula nas métricas."""
        if next_pos is None:
            return
        risk = self._danger(next_pos)
        self.collector.record_step(risk)
        self.position = next_pos

    def has_reached_goal(self) -> bool:
        return self.position == self.goal

    # ------------------------------------------------------------------ #
    # Fallback para quando não há caminho até a saída (FAQ item 7)
    # ------------------------------------------------------------------ #

    def fallback_move(self) -> tuple[int, int] | None:
        """
        Descida local: move para o vizinho de menor perigo fuzzy.
        Se o perigo atual for baixo (< 0.3), permanece parado para ganhar tempo.
        Retorna None se completamente cercado (falha registrada pelo collector).
        """
        p = self.perceive()
        if p["temperature"] < 30 and p["smoke"] < 0.3:
            return None  # espera — local relativamente seguro

        best_pos, best_danger = None, float("inf")
        for nx, ny in self.grid.neighbors(*self.position):
            if self.grid.is_walkable(nx, ny):
                d = self._danger((nx, ny))
                if d < best_danger:
                    best_danger, best_pos = d, (nx, ny)
        return best_pos

    # ------------------------------------------------------------------ #
    # Helpers internos
    # ------------------------------------------------------------------ #

    def _danger(self, pos: tuple[int, int]) -> float:
        x, y = pos
        return self.fuzzy.compute_danger(
            self.fire.get_temperature(x, y, self.grid),
            self.fire.get_smoke_density(x, y, self.grid),
            self.fire.get_fire_distance(x, y, self.grid),
        )

    def _find_path(self) -> list[tuple[int, int]] | None:
        if self.algorithm == "greedy":
            return greedy_best_first(self.position, self.goal, self.grid)
        # astar_fuzzy usa alpha; astar puro passa alpha=0
        effective_alpha = self.alpha if self.algorithm == "astar_fuzzy" else 0.0
        return astar(self.position, self.goal, self.grid, self._danger, alpha=effective_alpha)
