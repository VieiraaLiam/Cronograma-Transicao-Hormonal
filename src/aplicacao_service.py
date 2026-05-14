from datetime import datetime, timedelta
from aplicacao_dto import AplicacaoDTO
from aplicacao_repository import AplicacaoRepository
import config_repository

class AplicacaoService:
    def __init__(self, repositorio=None):
        self.config_repo = config_repository.ConfigRepository()
        self.repositorio = repositorio if repositorio is not None else AplicacaoRepository()
        self.ciclo_padrao = self.config_repo.get_ciclo_padrao()

    def registrar(self, data: str, ml: float, lado: str, notas: str = ""):
        if ml <= 0:
            raise ValueError("Dosagem deve ser maior que zero")
        
        # Calcula a próxima data usando o ciclo padrão
        proxima_data = self.calcular_proxima_data(data, self.ciclo_padrao)
        
        app = AplicacaoDTO(
            data=data,
            ml=ml,
            lado=lado,
            ciclo_dias=self.ciclo_padrao,
            proxima_data=proxima_data,  # ← NOVO
            notas=notas
        )
        self.repositorio.adicionar(app)
        return app

    def calcular_proxima_data(self, data_str: str, ciclo_dias: int) -> str:
        data = datetime.strptime(data_str, "%d/%m/%Y")
        proxima = data + timedelta(days=ciclo_dias)
        return proxima.strftime("%d/%m/%Y")
    
    def calcular_dias_restantes(self, data_str: str, ciclo_dias: int) -> int:
        hoje = datetime.now()
        proxima = datetime.strptime(self.calcular_proxima_data(data_str, ciclo_dias), "%d/%m/%Y")
        dias = (proxima - hoje).days
        return max(0, dias)
    
    def listar_todas(self):
        return self.repositorio.carregar_todas()
    
    def buscar_por_data(self, data: str):
        todas = self.listar_todas()
        if not todas:
            return []
        return [app for app in todas if app.data == data]