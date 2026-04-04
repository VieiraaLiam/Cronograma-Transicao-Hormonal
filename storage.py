import json
import datetime
from pathlib import Path
from model import Aplicacao

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar.events"]
CREDENTIALS_FILE = Path("credentials.json") # baixar do google cloud
TOKEN_FILE = Path("token.json")
CALENDAR_ID = "primary"  # ou o ID do calendário específico         

def get_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    return build("calendar", "v3", credentials=creds)

def create_all_day_event(date_str, summary=str, descripition: str="") -> dict:
    # date_str cria evento all day naquela data
    # retorna resposta da API
    dt = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
    start_date = dt.isoformat()
    end_date = (dt + datetime.timedelta(days=1)).isoformat() # end é exclusivo 
    service = get_service()
    event = {
        "summary": summary,
        "description": descripition,
        "start": {"date": start_date},
        "end": {"date": end_date},
    }
    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

def create_event_for_aplicacao(aplicacao) -> dict:
# Cria evento no Google Calendar para a próxima aplicação
    proxima = aplicacao.proxima_aplicacao()
    titulo = f"Aplicação {aplicacao.ml}ml ({aplicacao.lado})"
    descricao = getattr(aplicacao, "notas", "")
    return create_all_day_event(proxima, titulo, descricao)

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