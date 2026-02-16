# Cronograma - Transição Hormonal 🏥

Um aplicativo GUI simples em Python com Tkinter para gerenciar e acompanhar aplicações de hormônios durante a transição hormonal.

## Funcionalidades

- ✅ Registrar aplicações (data, dosagem, lado, ciclo)
- ✅ Calcular próxima aplicação automaticamente
- ✅ Exibir dias restantes para a próxima dose
- ✅ Histórico persistente em JSON
- ✅ Interface amigável com temas personalizados

## Estrutura do Projeto

```
Cronograma Transição Hormonal/
├── main.py              # Entry point
├── gui.py               # Interface Tkinter (MVC)
├── model.py             # Modelos de dados
├── storage.py           # Persistência JSON
├── tests/               # Testes unitários
├── data/                # Dados salvos (gerado automaticamente)
├── requirements.txt     # Dependências
└── README.md            # Este arquivo
```

## Como Executar

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/Cronograma-Transicao-Hormonal.git
cd "Cronograma Transição Hormonal"
```

### 2. Criar ambiente virtual (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 4. Executar a aplicação
```powershell
python main.py
```

### 5. Rodar testes (opcional)
```powershell
python -m pytest -q
```

## Dependências

- `Python 3.10+`
- `tkinter` (incluído no Python)
- `pytest` (desenvolvimento)
- `tkcalendar` 

## Autor

Desenvolvido com ❤️ para acompanhar a transição hormonal.

---

**Última atualização:** Fevereiro 2026
