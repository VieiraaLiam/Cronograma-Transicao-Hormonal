from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass
class Aplicacao:
    """Representa uma aplicação de hormônio."""
    data: str  # formato: DD/MM/YYYY
    ml: float
    lado: str  # "esquerdo" ou "direito"
    ciclo_dias: int
    
    def proxima_aplicacao(self) -> str:
        """Calcula a data da próxima aplicação."""
        try:
            data_obj = datetime.strptime(self.data, "%d/%m/%Y")
            proxima = data_obj + timedelta(days=self.ciclo_dias)
            return proxima.strftime("%d/%m/%Y")
        except ValueError:
            return "Data inválida"
    
    def dias_restantes(self) -> int:
        """Retorna quantos dias faltam para a próxima aplicação."""
        try:
            data_obj = datetime.strptime(self.data, "%d/%m/%Y")
            proxima = data_obj + timedelta(days=self.ciclo_dias)
            restante = (proxima - datetime.now()).days
            return max(0, restante)
        except ValueError:
            return -1  # Indica data inválida