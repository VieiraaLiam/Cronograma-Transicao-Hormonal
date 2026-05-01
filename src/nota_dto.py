class NotaDTO:
    def __init__(self, data: str, texto: str, horario: str = None):
        self.data = data
        self.texto = texto
        self.horario = horario