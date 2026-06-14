"""Overlay heatmap de perigo fuzzy sobre o grid (verde → amarelo → vermelho)."""
import pygame


def render_heatmap(
    surface: pygame.Surface,
    fuzzy_values: dict[tuple[int, int], float],
    cell_size: int = 60,
    alpha: int = 130,
) -> None:
    """Desenha uma camada semitransparente colorida pelo nível de perigo de cada célula."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    for (x, y), danger in fuzzy_values.items():
        r, g, b = danger_to_color(danger)
        pygame.draw.rect(overlay, (r, g, b, alpha),
                         (x * cell_size, y * cell_size, cell_size - 1, cell_size - 1))
    surface.blit(overlay, (0, 0))


def danger_to_color(danger: float) -> tuple[int, int, int]:
    """Interpola a cor no gradiente verde(0) → amarelo(0.5) → vermelho(1)."""
    danger = max(0.0, min(1.0, danger))
    if danger <= 0.5:
        r = int(255 * danger * 2)
        g = 200
    else:
        r = 255
        g = int(200 * (1.0 - (danger - 0.5) * 2))
    return (r, g, 0)
