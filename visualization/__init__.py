"""
Pacote visualization — renderização pygame do ambiente e métricas visuais.

Exporta o Renderer para o loop de visualização em tempo real e a
função render_heatmap para sobreposição do mapa de calor de risco fuzzy.
"""
from visualization.renderer import Renderer
from visualization.heatmap import render_heatmap

__all__ = ["Renderer", "render_heatmap"]
