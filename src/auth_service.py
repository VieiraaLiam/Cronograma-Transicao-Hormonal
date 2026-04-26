from login_dto import LoginDTO
from token_repository import TokenRepository

class AuthService:
    def __init__(self, repositorio=None):
        self.repositorio = repositorio if repositorio is not None else TokenRepository()
    
    def login_simulado(self, email: str):
        if not email or "@" not in email:
            print("❌ Email inválido")
            return None
        
        nome = email.split("@")[0]
        token = f"fake_token_{email}"
        
        return LoginDTO(email=email, nome=nome, token=token)
    
    def salvar_credenciais(self, login):
        return self.repositorio.salvar(login.to_dict())
    
    def carregar_credenciais(self):
        dados = self.repositorio.carregar()
        return LoginDTO.from_dict(dados) if dados else None
    
    def logout(self):
        return self.repositorio.deletar()
    
    def esta_logado(self):
        return self.repositorio.carregar() is not None