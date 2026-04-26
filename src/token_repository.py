import json
import os

class TokenRepository:
    def __init__(self, caminho_arquivo: str = "data/token.json"):
        self.caminho = caminho_arquivo
        self._garantir_pasta()
    
    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho)
        if pasta and not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def salvar(self, dados):
        try:
            with open(self.caminho, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar token: {e}")
            return False
    
    def carregar(self):
        if not os.path.exists(self.caminho):
            return None
        try:
            with open(self.caminho, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar token: {e}")
            return None
    
    def deletar(self):
        if os.path.exists(self.caminho):
            os.remove(self.caminho)
            return True
        return False