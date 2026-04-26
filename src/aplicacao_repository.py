import json
import os
from aplicacao_dto import AplicacaoDTO

class AplicacaoRepository:
    def __init__(self, caminho_arquivo: str = "data/aplicacoes.json"):
        self.caminho = caminho_arquivo
        self._garantir_pasta()
    
    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def salvar_todas(self, aplicacoes):
        try:
            dados = [app.to_dict() for app in aplicacoes]
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar aplicações: {e}")
            return False
    
    def carregar_todas(self):
        if not os.path.exists(self.caminho):
            return []
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return [AplicacaoDTO.from_dict(item) for item in dados]
        except Exception as e:
            print(f"Erro ao carregar aplicações: {e}")
            return []
    
    def adicionar(self, aplicacao):
        todas = self.carregar_todas()
        todas.append(aplicacao)
        return self.salvar_todas(todas)