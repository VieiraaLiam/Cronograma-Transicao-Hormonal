import json
import os 

class ConfigRepository:
    def __init__(self, caminho_arquivo="data/config.json"):
        self.caminho_arquivo = caminho_arquivo
        self.config = self.carregar_config()

    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho_arquivo)
        if not os.path.exists(pasta):
            os.makedirs(pasta)

    def carregar_config(self):
        if os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "r") as f:
                return json.load(f)
        return {}

    def salvar_config(self):
        self._garantir_pasta()
        with open(self.caminho_arquivo, "w") as f:
            json.dump(self.config, f, indent=4)

    def set_ciclo_padrao(self, ciclo: int):
        self.config["ciclo_padrao"] = ciclo
        self.salvar_config()

    def get_ciclo_padrao(self) -> int:
        return self.config.get("ciclo_padrao", 30)