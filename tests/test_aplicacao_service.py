import tempfile
from aplicacao_service import AplicacaoService
from aplicacao_repository import AplicacaoRepository
import config_repository
import os

def test_registrar_aplicacao():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Configura caminhos temporários
        config_repo = config_repository.ConfigRepository(os.path.join(tmpdir, "config.json"))
        config_repo.set_ciclo_padrao(21)
        
        app_repo = AplicacaoRepository(os.path.join(tmpdir, "aplicacoes.json"))
        service = AplicacaoService(app_repo)
        
        # Força o ciclo para 21 (substitui o config real)
        service.ciclo_padrao = 21
        
        app = service.registrar("01/05/2026", 0.5, "direito", "Nota teste")
        
        assert app.data == "01/05/2026"
        assert app.ml == 0.5
        assert app.lado == "direito"
        assert app.ciclo_dias == 21
        assert app.proxima_data == "22/05/2026"

def test_calcular_proxima_data():
    service = AplicacaoService()
    service.ciclo_padrao = 21
    
    proxima = service.calcular_proxima_data("01/05/2026", 21)
    assert proxima == "22/05/2026"