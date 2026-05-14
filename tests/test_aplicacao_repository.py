import os
import tempfile
from aplicacao_dto import AplicacaoDTO
from aplicacao_repository import AplicacaoRepository

def test_adicionar_e_listar():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "aplicacoes.json")
        repo = AplicacaoRepository(caminho)
        
        app1 = AplicacaoDTO("01/05/2026", 0.5, "direito", 21, "22/05/2026", "")
        app2 = AplicacaoDTO("15/05/2026", 0.6, "esquerdo", 21, "05/06/2026", "Teste")
        
        repo.adicionar(app1)
        repo.adicionar(app2)
        
        todas = repo.carregar_todas()
        assert len(todas) == 2
        assert todas[0].data == "01/05/2026"
        assert todas[1].ml == 0.6

def test_atualizar():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "aplicacoes.json")
        repo = AplicacaoRepository(caminho)
        
        app = AplicacaoDTO("01/05/2026", 0.5, "direito", 21, "22/05/2026", "Original")
        repo.adicionar(app)
        
        # Atualiza
        app_atualizado = AplicacaoDTO("01/05/2026", 0.5, "direito", 21, "25/05/2026", "Atualizado")
        repo.atualizar(app_atualizado)
        
        todas = repo.carregar_todas()
        assert todas[0].proxima_data == "25/05/2026"
        assert todas[0].notas == "Atualizado"

def test_remover():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "aplicacoes.json")
        repo = AplicacaoRepository(caminho)
        
        app = AplicacaoDTO("01/05/2026", 0.5, "direito", 21, "22/05/2026", "")
        repo.adicionar(app)
        
        repo.remover(app)
        todas = repo.carregar_todas()
        assert len(todas) == 0