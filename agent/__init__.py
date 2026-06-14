"""
Pacote agent — loop perceive-think-act do agente inteligente MIRA.

Exporta a classe Agent, responsável pelo ciclo de percepção do ambiente,
decisão de ação via busca heurística com avaliação fuzzy e execução
do movimento com suporte a replanejamento dinâmico.
"""
from agent.agent import Agent

__all__ = ["Agent"]
