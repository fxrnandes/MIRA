"""
Pacote metrics — coleta e análise de métricas de desempenho do MIRA.

Exporta o MetricsCollector para registro em tempo de execução e
geração de relatório comparativo entre os algoritmos de busca.
"""
from metrics.collector import MetricsCollector

__all__ = ["MetricsCollector"]
