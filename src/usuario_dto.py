class UsuarioDTO:
    def __init__(self, email: str, senha_hash: str, google_token: str = None):
        self.email = email
        self.senha_hash = senha_hash
        self.google_token = google_token

    def to_dict(self):
        return {
            "email": self.email,
            "senha_hash": self.senha_hash,
            "google_token": self.google_token
        }
    
    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return UsuarioDTO(
            email=data.get("email", ""),
            senha_hash=data.get("senha_hash", ""),
            google_token=data.get("google_token")
        )