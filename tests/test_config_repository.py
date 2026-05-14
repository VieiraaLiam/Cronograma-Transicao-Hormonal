import os
import tempfile
from config_repository import ConfigRepository

def test_criar_config_repository():
    # Cria um arquivo temporário para teste
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "config.json")
        repo = ConfigRepository(caminho)
        
        # Testa ciclo padrão
        ciclo = repo.get_ciclo_padrao()
        assert ciclo == 30  # Valor padrão
        
        # Altera e testa
        repo.set_ciclo_padrao(21)
        assert repo.get_ciclo_padrao() == 21