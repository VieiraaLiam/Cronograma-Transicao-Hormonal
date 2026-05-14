import os
import tempfile
from nota_repository import NotaRepository

def test_adicionar_e_listar_notas():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "notas.json")
        repo = NotaRepository(caminho)
        
        # Adiciona notas
        repo.adicionar("01/05/2026", "Acordei bem", "08:30")
        repo.adicionar("01/05/2026", "Tontura leve", "14:00")
        repo.adicionar("02/05/2026", "Cansaço", "09:15")
        
        # Verifica notas do dia 01/05
        notas = repo.listar_por_data("01/05/2026")
        assert len(notas) == 2
        
        textos = [f"{nota.horario} - {nota.texto}" for nota in notas]
        assert "08:30 - Acordei bem" in textos
        assert "14:00 - Tontura leve" in textos
        
        # Verifica notas do dia 02/05
        notas = repo.listar_por_data("02/05/2026")
        assert len(notas) == 1
        assert notas[0].horario == "09:15"
        assert "Cansaço" in notas[0].texto
        
        # Verifica todas as notas
        todas = repo.listar_todas()
        assert len(todas) == 3

def test_adicionar_nota_sem_horario():
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho = os.path.join(tmpdir, "notas.json")
        repo = NotaRepository(caminho)
        
        # Adiciona nota sem horário (deve gerar automático)
        repo.adicionar("01/05/2026", "Nota sem horário")
        
        notas = repo.listar_por_data("01/05/2026")
        assert len(notas) == 1
        assert notas[0].texto == "Nota sem horário"
        assert notas[0].horario is not None  # Horário foi gerado