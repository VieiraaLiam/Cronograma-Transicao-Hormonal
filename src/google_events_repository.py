import json
import os

class GoogleEventsRepository:
    def __init__(self, caminho_arquivo="data/google_events.json"):
        self.caminho_arquivo = caminho_arquivo
        self._garantir_pasta()
    
    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def _carregar(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r") as f:
                return json.load(f)
        return {}
    
    def _salvar(self, dados):
        with open(self.caminho_arquivo, "w") as f:
            json.dump(dados, f, indent=4)
    
    def salvar_evento(self, data: str, event_id: str):
        dados = self._carregar()
        dados[data] = event_id
        self._salvar(dados)
    
    def buscar_evento_por_data(self, data: str):
        dados = self._carregar()
        return dados.get(data)
    
    def deletar_evento_por_data(self, data: str):
        dados = self._carregar()
        if data in dados:
            del dados[data]
            self._salvar(dados)
            return True
        return False
    
    def listar_todos(self):
        return self._carregar()
    

