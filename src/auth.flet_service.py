import hashlib
from usuario_repository import UsuarioRepository
from usuario_dto import UsuarioDTO

class AuthServiceFlet:
    def __init__(self):
        self.repo = UsuarioRepository()

    def _hash_senha(self, senha: str) -> str:
        # Cria um hash da senha usando SHA-256
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def registrar(self, email: str, senha: str) -> bool:
        # Registra novo usuário
        if not email or not senha:
            return False  # Email e senha são obrigatórios
        
    # Verifica se o email já está registrado
        if self.repo.buscar_por_email(email):
            return False 
        
    # Cria novo usuário
        usuario = self.repo.buscar_por_email(email)
        if not usuario:
            return None
        
        senha_hash = self._hash_senha(senha)
        if usuario.senha_hash == senha_hash:
            return usuario
        
        return None
    
    def vincular_google(self, email: str, google_token: str) -> bool:
        # Vincula token do google a um usuário
        usuario = self.repo.buscar_por_email(email)
        if not usuario:
            return False
        
        usuario.google_token = google_token
        return self.repo.salvar(usuario)

