import json
import os
from aplicacao_dto import AplicacaoDTO

class AplicacaoRepository:
    def __init__(self, caminho_arquivo="data/aplicacoes.json"):
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
    
    def remover(self, aplicacao):
        """Remove uma aplicação específica da lista"""
        todas = self.carregar_todas()
        for i, app in enumerate(todas):
            if (app.data == aplicacao.data and 
                app.ml == aplicacao.ml and 
                app.lado == aplicacao.lado):
                del todas[i]
                return self.salvar_todas(todas)
        return False
    
    def atualizar(self, aplicacao_atualizada):  # ← NOVO MÉTODO
        """Substitui uma aplicação existente pela versão atualizada"""
        todas = self.carregar_todas()
        encontrou = False
        
        for i, app in enumerate(todas):
            # Identifica a aplicação única por data, dosagem e lado
            if (app.data == aplicacao_atualizada.data and 
                app.ml == aplicacao_atualizada.ml and 
                app.lado == aplicacao_atualizada.lado):
                todas[i] = aplicacao_atualizada
                encontrou = True
                break
        
        if encontrou:
            return self.salvar_todas(todas)
        return False