from datetime import datetime, timedelta
from aplicacao_dto import AplicacaoDTO
from aplicacao_repository import AplicacaoRepository

class AplicacaoService:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio if repositorio is not None else AplicacaoRepository()
    
    def registrar(self, data: str, ml: float, lado: str, ciclo_dias: int, notas: str = ""):
        if ml <= 0:
            raise ValueError("Dosagem deve ser maior que zero")
        if ciclo_dias <= 0:
            raise ValueError("Ciclo deve ser maior que zero")
        
        app = AplicacaoDTO(data=data, ml=ml, lado=lado, ciclo_dias=ciclo_dias, notas=notas)
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