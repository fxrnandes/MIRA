"""
Configuração raiz do pytest para o projeto MIRA.

Garante que o diretório do projeto esteja no sys.path, permitindo
que os módulos (world, fuzzy, search, etc.) sejam importados
corretamente pelos testes em tests/.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
