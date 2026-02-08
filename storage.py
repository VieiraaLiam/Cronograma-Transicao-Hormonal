import json
from pathlib import Path
from model import Aplicacao


DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
SCHEDULE_FILE = DATA_DIR / "schedule.json"


def carregar_aplicacoes():
    """Carrega todas as aplicações salvas."""
    if not SCHEDULE_FILE.exists():
        return []
    try:
        conteudo = SCHEDULE_FILE.read_text(encoding="utf-8")
        dados = json.loads(conteudo)
        return [Aplicacao(**item) for item in dados]
    except (json.JSONDecodeError, KeyError, ValueError):
        return []


def salvar_aplicacoes(aplicacoes):
    """Salva todas as aplicações."""
    dados = [
        {
            "data": app.data,
            "ml": app.ml,
            "lado": app.lado,
            "ciclo_dias": app.ciclo_dias,
        }
        for app in aplicacoes
    ]
    SCHEDULE_FILE.write_text(
        json.dumps(dados, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def adicionar_aplicacao(aplicacao):
    """Adiciona uma nova aplicação."""
    aplicacoes = carregar_aplicacoes()
    aplicacoes.append(aplicacao)
    salvar_aplicacoes(aplicacoes)