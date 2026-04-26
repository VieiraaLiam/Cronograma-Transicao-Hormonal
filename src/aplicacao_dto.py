class AplicacaoDTO:
    def __init__(self, data: str, ml: float, lado: str, ciclo_dias: int, notas: str = ""):
        self.data = data
        self.ml = ml
        self.lado = lado
        self.ciclo_dias = ciclo_dias
        self.notas = notas
    
    def to_dict(self):
        return {
            "data": self.data,
            "ml": self.ml,
            "lado": self.lado,
            "ciclo_dias": self.ciclo_dias,
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
            notas=data.get("notas", "")
        )