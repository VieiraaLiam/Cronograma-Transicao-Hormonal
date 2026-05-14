class AplicacaoDTO:
    def __init__(self, data, ml, lado, ciclo_dias, proxima_data, notas=""):
        self.data = data
        self.ml = ml
        self.lado = lado
        self.ciclo_dias = ciclo_dias
        self.proxima_data = proxima_data
        self.notas = notas
    
    def to_dict(self):
        return {
            "data": self.data,
            "ml": self.ml,
            "lado": self.lado,
            "ciclo_dias": self.ciclo_dias,
            "proxima_data": self.proxima_data,  # ← ADICIONADO
            "notas": self.notas
        }
    
    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return AplicacaoDTO(
            data=data.get("data", ""),
            ml=float(data.get("ml", 0)),
            lado=data.get("lado", ""),
            ciclo_dias=int(data.get("ciclo_dias", 7)),
            proxima_data=data.get("proxima_data", ""),  # ← ADICIONADO
            notas=data.get("notas", "")
        )