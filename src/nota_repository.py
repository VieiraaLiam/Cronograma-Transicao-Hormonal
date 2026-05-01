import json
import os 
from datetime import datetime
from nota_dto import NotaDTO

class NotaRepository:
    def __init__(self, caminho_arquivo="data/notas.json"):
        self.caminho_arquivo = caminho_arquivo
        self._garantir_pasta()
    
    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def carregar(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r") as f:
                dados = json.load(f)
                return [NotaDTO(**nota) for nota in dados]
        return []
    
    def salvar(self, dados):
        self._garantir_pasta()
        # Converte objetos para dicionários
        dados_dict = [{"data": n.data, "texto": n.texto, "horario": n.horario} for n in dados]
        with open(self.caminho_arquivo, "w") as f:
            json.dump(dados_dict, f, indent=4)
    
    def adicionar(self, data: str, texto: str, horario: str = None):
        if horario is None:
            horario = datetime.now().strftime("%H:%M")
        
        notas = self.carregar()
        nova_nota = NotaDTO(data=data, texto=texto, horario=horario)
        notas.append(nova_nota)
        self.salvar(notas)
    
    def listar_por_data(self, data: str):
        notas = self.carregar()
        return [nota for nota in notas if nota.data == data]
    
    def listar_todas(self):
        return self.carregar()