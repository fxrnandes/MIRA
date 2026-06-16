"""Renderização pygame com tema escuro, animações e painel de informações."""
import math
import pygame
from world.grid import Grid
from world.cell import CellType
from visualization.heatmap import render_heatmap, danger_to_color

CELL  = 60   # pixels por célula
HUD_H = 68   # altura do painel de info na parte de baixo
FPS   = 5

# Paleta de cores
_FREE  = (215, 213, 195)
_WALL  = (40,  42,  54)
_SMOKE = (118, 120, 132)
_START = (200, 198, 180)
_BG    = (22,  22,  32)
_HUD   = (16,  16,  26)
_AGENT = (35,  108, 228)
_GLOW  = (80,  148, 255)
_PATH  = (110, 168, 255)


class Renderer:
    def __init__(self, grid: Grid, algorithm: str = "", title: str = "MIRA — Evacuação Inteligente") -> None:
        pygame.init()
        self.grid = grid
        self.algorithm = algorithm
        w = grid.width * CELL
        h = grid.height * CELL + HUD_H
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self._font    = pygame.font.SysFont("segoeui", 16, bold=True)
        self._font_sm = pygame.font.SysFont("segoeui", 13)
        self._restart_btn = pygame.Rect(0, 0, 0, 0)  # atualizado em _draw_hud

    # ------------------------------------------------------------------ #

    def render(
        self,
        agent_pos: tuple[int, int] | None = None,
        path: list[tuple[int, int]] | None = None,
        fuzzy_values: dict[tuple[int, int], float] | None = None,
        step: int = 0,
        danger: float = 0.0,
        replans: int = 0,
        awaiting_rescue: bool = False,
    ) -> None:
        t = pygame.time.get_ticks() / 1000.0
        self.screen.fill(_BG)

        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self._draw_cell(x, y, t)

        if fuzzy_values:
            render_heatmap(self.screen, fuzzy_values, CELL)

        if path:
            for px, py in path:
                cx = px * CELL + CELL // 2
                cy = py * CELL + CELL // 2
                pygame.draw.circle(self.screen, _PATH, (cx, cy), 5)

        if agent_pos:
            self._draw_agent(agent_pos, t)

        if awaiting_rescue:
            self._draw_rescue_banner(t)

        self._draw_hud(step, danger, replans)
        pygame.display.flip()
        self.clock.tick(FPS)

    def _draw_rescue_banner(self, t: float) -> None:
        """Banner de alerta no topo: sem rota de saída, aguardando resgate."""
        sw = self.screen.get_width()
        pulse = 0.5 + 0.5 * math.sin(t * 4.0)
        bh = 40

        banner = pygame.Surface((sw, bh), pygame.SRCALPHA)
        banner.fill((180, 40, 40, int(170 + 60 * pulse)))
        self.screen.blit(banner, (0, 0))
        pygame.draw.line(self.screen, (255, 120, 120), (0, bh), (sw, bh), 2)

        msg = "⚠ SEM ROTA DE SAÍDA — AGUARDANDO RESGATE"
        lbl = self._font.render(msg, True, (255, 240, 240))
        self.screen.blit(lbl, ((sw - lbl.get_width()) // 2,
                               (bh - lbl.get_height()) // 2))

    # ------------------------------------------------------------------ #

    def _draw_cell(self, x: int, y: int, t: float) -> None:
        ct  = self.grid.get_cell(x, y)
        rx  = x * CELL
        ry  = y * CELL
        rec = pygame.Rect(rx, ry, CELL - 1, CELL - 1)

        if ct == CellType.FIRE:
            flicker = 0.5 + 0.5 * math.sin(t * 9.0 + x * 1.7 + y * 1.3)
            base    = (220, int(38 + flicker * 112), int(flicker * 14))
            pygame.draw.rect(self.screen, base, rec)
            # núcleo mais claro
            inner = rec.inflate(-(CELL // 3), -(CELL // 3))
            core  = (min(255, base[0] + 28), min(255, base[1] + 72), 0)
            pygame.draw.rect(self.screen, core, inner)

        elif ct == CellType.EXIT:
            pulse = 0.6 + 0.4 * math.sin(t * 3.0)
            g_val = int(148 + pulse * 62)
            pygame.draw.rect(self.screen, (28, g_val, 52), rec)
            lbl = self._font.render("S", True, (255, 255, 255))
            self.screen.blit(lbl, (rx + (CELL - lbl.get_width()) // 2,
                                   ry + (CELL - lbl.get_height()) // 2))

        elif ct == CellType.SMOKE:
            pygame.draw.rect(self.screen, _SMOKE, rec)
            for i in range(3):
                off = int(math.sin(t * 1.6 + i * 2.1) * 4)
                sx  = rx + CELL // 5 + i * (CELL // 3) + off
                sy  = ry + CELL // 2 + off
                pygame.draw.circle(self.screen, (148, 152, 164), (sx, sy), 4)

        elif ct == CellType.WALL:
            pygame.draw.rect(self.screen, _WALL, rec)
            pygame.draw.rect(self.screen, (56, 58, 72), rec, 1)

        elif ct == CellType.AGENT_START:
            pygame.draw.rect(self.screen, _START, rec)

        else:
            pygame.draw.rect(self.screen, _FREE, rec)

    def _draw_agent(self, pos: tuple[int, int], t: float) -> None:
        ax, ay = pos
        cx = ax * CELL + CELL // 2
        cy = ay * CELL + CELL // 2
        r  = CELL // 3

        # halo pulsante
        glow = pygame.Surface((CELL * 2, CELL * 2), pygame.SRCALPHA)
        pulse = int(28 + 22 * math.sin(t * 4.5))
        for i in range(3, 0, -1):
            pygame.draw.circle(glow, (*_GLOW, pulse // i),
                               (CELL, CELL), r + i * 6)
        self.screen.blit(glow, (cx - CELL, cy - CELL))

        # corpo
        pygame.draw.circle(self.screen, _AGENT, (cx, cy), r)
        pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), r, 2)
        # olho
        pygame.draw.circle(self.screen, (205, 232, 255),
                           (cx, cy - r // 3), r // 4)

    def _draw_hud(self, step: int, danger: float, replans: int) -> None:
        hy = self.grid.height * CELL
        sw = self.screen.get_width()

        pygame.draw.rect(self.screen, _HUD, (0, hy, sw, HUD_H))
        pygame.draw.line(self.screen, (52, 54, 72), (0, hy), (sw, hy), 1)

        # — lado esquerdo: algoritmo e passo
        alg = self.algorithm.replace("_", " ").upper()
        self.screen.blit(self._font.render(alg, True, (165, 200, 255)), (14, hy + 10))
        self.screen.blit(
            self._font_sm.render(f"Passo: {step}   Replans: {replans}",
                                 True, (140, 140, 175)),
            (14, hy + 36),
        )

        # — lado direito: barra de perigo
        bx = sw // 2 + 50
        by = hy + 12
        bw = sw - bx - 55
        bh = 16

        self.screen.blit(
            self._font_sm.render("Perigo:", True, (140, 140, 175)),
            (sw // 2, hy + 14),
        )

        pygame.draw.rect(self.screen, (48, 50, 65), (bx, by, bw, bh), border_radius=5)
        fill = int(bw * max(0.0, min(1.0, danger)))
        if fill > 0:
            pygame.draw.rect(self.screen, danger_to_color(danger),
                             (bx, by, fill, bh), border_radius=5)
        pygame.draw.rect(self.screen, (88, 90, 108), (bx, by, bw, bh), 1, border_radius=5)

        self.screen.blit(
            self._font_sm.render(f"{int(danger * 100)}%", True, (195, 198, 215)),
            (bx + bw + 6, by),
        )

        self._draw_restart_button()

    def _draw_restart_button(self) -> None:
        hy  = self.grid.height * CELL
        bw, bh = 110, 30
        bx  = self.screen.get_width() // 2 - bw - 20
        by  = hy + (HUD_H - bh) // 2
        self._restart_btn = pygame.Rect(bx, by, bw, bh)

        hover = self._restart_btn.collidepoint(pygame.mouse.get_pos())
        bg    = (52, 96, 188) if hover else (38, 70, 142)
        pygame.draw.rect(self.screen, bg, self._restart_btn, border_radius=6)
        pygame.draw.rect(self.screen, (110, 168, 255), self._restart_btn, 1, border_radius=6)

        lbl = self._font_sm.render("Reiniciar (R)", True, (225, 235, 255))
        self.screen.blit(lbl, (bx + (bw - lbl.get_width()) // 2,
                               by + (bh - lbl.get_height()) // 2))

    def wait_for_start(
        self,
        agent_pos: tuple[int, int] | None = None,
        fuzzy_values: dict[tuple[int, int], float] | None = None,
    ) -> str:
        """Mostra o estado inicial com um overlay e bloqueia até o usuário
        apertar qualquer tecla ou clicar. Retorna 'running' para iniciar
        ou 'quit' se ele fechar a janela / apertar ESC."""
        font_big = pygame.font.SysFont("segoeui", 34, bold=True)
        msg   = "Aperte qualquer tecla para iniciar"
        msg_x = "ESC ou fechar para sair"

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                    return "running"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return "running"

            t = pygame.time.get_ticks() / 1000.0

            # desenha o cenário de fundo
            self.screen.fill(_BG)
            for y in range(self.grid.height):
                for x in range(self.grid.width):
                    self._draw_cell(x, y, t)
            if fuzzy_values:
                render_heatmap(self.screen, fuzzy_values, CELL)
            if agent_pos:
                self._draw_agent(agent_pos, t)
            self._draw_hud(0, 0.0, 0)

            # véu escuro por cima
            sw, sh = self.screen.get_size()
            veil = pygame.Surface((sw, sh), pygame.SRCALPHA)
            veil.fill((10, 10, 18, 170))
            self.screen.blit(veil, (0, 0))

            # texto pulsante
            pulse = 0.6 + 0.4 * math.sin(t * 3.0)
            color = (int(180 + 75 * pulse), int(200 + 55 * pulse), 255)
            label = font_big.render(msg, True, color)
            self.screen.blit(label, ((sw - label.get_width()) // 2,
                                     (sh - label.get_height()) // 2 - 18))
            sub = self._font_sm.render(msg_x, True, (150, 152, 175))
            self.screen.blit(sub, ((sw - sub.get_width()) // 2,
                                   (sh - label.get_height()) // 2 + 28))

            pygame.display.flip()
            self.clock.tick(FPS)

    # ------------------------------------------------------------------ #

    def handle_events(self) -> str:
        """Retorna 'running', 'quit' ou 'restart'."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                if event.key == pygame.K_r:
                    return "restart"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._restart_btn.collidepoint(event.pos):
                    return "restart"
        return "running"

    def close(self) -> None:
        pygame.quit()
