"""
MIRA — Modelo Inteligente de Rota Autônoma
Uso: python main.py --scenario scenarios/basic.json --algorithm astar_fuzzy --alpha 0.5
"""
import argparse
import time

from world.map_loader import load_scenario
from world.cell import CellType
from dynamics.fire_automaton import FireAutomaton
from fuzzy.inference import FuzzyInferenceSystem
from agent.agent import Agent
from visualization.renderer import Renderer
from metrics.collector import MetricsCollector


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="MIRA — Evacuação com Fuzzy + A*",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--scenario",   default="scenarios/basic.json",
                   help="Caminho para o arquivo JSON do cenário")
    p.add_argument("--algorithm",  default="astar_fuzzy",
                   choices=["astar_fuzzy", "astar", "greedy"],
                   help="Algoritmo de busca")
    p.add_argument("--alpha",      type=float, default=0.5,
                   help="Peso do risco fuzzy na função de custo (0=distância pura, 1=só risco)")
    p.add_argument("--visualize",  action=argparse.BooleanOptionalAction, default=True,
                   help="Habilita a janela pygame")
    p.add_argument("--max-steps",  type=int, default=500,
                   help="Limite máximo de passos por episódio")
    return p.parse_args()


def find_positions(grid) -> tuple[tuple[int, int], tuple[int, int]]:
    """Varre o grid para encontrar AGENT_START e EXIT."""
    start = goal = None
    for y in range(grid.height):
        for x in range(grid.width):
            ct = grid.get_cell(x, y)
            if ct == CellType.AGENT_START:
                start = (x, y)
            elif ct == CellType.EXIT:
                goal = (x, y)
    if start is None or goal is None:
        raise ValueError("O cenário precisa ter AGENT_START (5) e EXIT (4).")
    return start, goal


def compute_fuzzy_map(grid, fire, fuzzy) -> dict[tuple[int, int], float]:
    """Calcula o índice de perigo para cada célula não-parede (usado pelo heatmap)."""
    values = {}
    for y in range(grid.height):
        for x in range(grid.width):
            if grid.get_cell(x, y) != CellType.WALL:
                values[(x, y)] = fuzzy.compute_danger(
                    fire.get_temperature(x, y, grid),
                    fire.get_smoke_density(x, y, grid),
                    fire.get_fire_distance(x, y, grid),
                )
    return values


def run_episode(args: argparse.Namespace, renderer: Renderer | None) -> str:
    """Executa um episódio. Retorna 'quit' (fechar), 'restart' (reiniciar)
    ou 'done' (terminou normalmente)."""
    grid = load_scenario(args.scenario)
    start, goal = find_positions(grid)

    fire      = FireAutomaton(spread_prob=0.25, smoke_range=2)
    fuzzy     = FuzzyInferenceSystem()
    collector = MetricsCollector(args.algorithm, args.scenario)
    agent     = Agent(start, goal, grid, fire, fuzzy, collector,
                      algorithm=args.algorithm, alpha=args.alpha)

    print(f"[MIRA] Iniciando — algoritmo: {args.algorithm}, alpha: {args.alpha}")
    print(f"       Posição inicial: {start}  |  Saída: {goal}")

    if renderer:
        renderer.grid = grid  # janela reaproveitada entre reinícios
        initial_map = compute_fuzzy_map(grid, fire, fuzzy)
        action = renderer.wait_for_start(agent.position, initial_map)
        if action != "running":
            return action

    t0 = time.time()
    success = False

    for step in range(args.max_steps):
        next_pos = agent.decide()
        agent.act(next_pos)
        fire.step(grid)

        if agent.has_reached_goal():
            success = True
            print(f"[MIRA] Agente escapou em {step + 1} passos!")
            break

        if next_pos is None:
            print(f"[MIRA] Agente preso no passo {step + 1} — sem caminho disponível.")
            break

        if renderer:
            fuzzy_map = compute_fuzzy_map(grid, fire, fuzzy)
            ax, ay = agent.position
            current_danger = fuzzy.compute_danger(
                fire.get_temperature(ax, ay, grid),
                fire.get_smoke_density(ax, ay, grid),
                fire.get_fire_distance(ax, ay, grid),
            )
            renderer.render(
                agent.position, agent.plan[:], fuzzy_map,
                step=step + 1,
                danger=current_danger,
                replans=collector._current.replanning_count,
                awaiting_rescue=agent.awaiting_rescue,
            )
            event = renderer.handle_events()
            if event == "quit":
                print("[MIRA] Simulação encerrada pelo usuário.")
                return "quit"
            if event == "restart":
                print("[MIRA] Reiniciando simulação.")
                return "restart"
    else:
        print(f"[MIRA] Limite de {args.max_steps} passos atingido.")

    collector.record_execution_time(time.time() - t0)
    collector.finish_episode(success, collector._current.steps)

    print("\n" + collector.generate_report())

    if renderer:
        # Mantém a janela aberta até o usuário fechar ou reiniciar.
        # Preserva o mapa de perigo e o aviso de resgate, se aplicável.
        final_map = compute_fuzzy_map(grid, fire, fuzzy)
        while True:
            event = renderer.handle_events()
            if event == "quit":
                return "quit"
            if event == "restart":
                return "restart"
            renderer.render(agent.position, [], final_map,
                            awaiting_rescue=agent.awaiting_rescue)

    return "done"


def main() -> None:
    args = parse_args()

    print(f"[MIRA] Carregando cenário: {args.scenario}")
    renderer = Renderer(load_scenario(args.scenario),
                        algorithm=args.algorithm) if args.visualize else None

    while True:
        status = run_episode(args, renderer)
        if status != "restart":
            break

    if renderer:
        renderer.close()


if __name__ == "__main__":
    main()
