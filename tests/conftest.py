# tests/conftest.py
import sys
import os

# Adiciona a pasta src ao PATH para os testes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))