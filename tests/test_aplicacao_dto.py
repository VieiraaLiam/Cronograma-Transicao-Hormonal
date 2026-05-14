from aplicacao_dto import AplicacaoDTO

def test_criar_aplicacao_dto():
    app = AplicacaoDTO(
        data="01/05/2026",
        ml=0.5,
        lado="direito",
        ciclo_dias=21,
        proxima_data="22/05/2026",
        notas="Teste"
    )
    
    assert app.data == "01/05/2026"
    assert app.ml == 0.5
    assert app.lado == "direito"
    assert app.ciclo_dias == 21
    assert app.proxima_data == "22/05/2026"
    assert app.notas == "Teste"

def test_to_dict():
    app = AplicacaoDTO("01/05/2026", 0.5, "direito", 21, "22/05/2026", "Teste")
    dict_app = app.to_dict()
    
    assert dict_app["data"] == "01/05/2026"
    assert dict_app["ml"] == 0.5
    assert dict_app["lado"] == "direito"
    assert dict_app["ciclo_dias"] == 21
    assert dict_app["proxima_data"] == "22/05/2026"
    assert dict_app["notas"] == "Teste"

def test_from_dict():
    dados = {
        "data": "01/05/2026",
        "ml": 0.5,
        "lado": "direito",
        "ciclo_dias": 21,
        "proxima_data": "22/05/2026",
        "notas": "Teste"
    }
    app = AplicacaoDTO.from_dict(dados)
    
    assert app.data == "01/05/2026"
    assert app.ml == 0.5
    assert app.lado == "direito"
    assert app.ciclo_dias == 21
    assert app.proxima_data == "22/05/2026"
    assert app.notas == "Teste"

def test_from_dict_vazio():
    app = AplicacaoDTO.from_dict(None)
    assert app is None