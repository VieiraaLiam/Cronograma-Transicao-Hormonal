class LoginDTO:
    def __init__(self, email: str, nome: str, token: str):
        self.email = email
        self.nome = nome
        self.token = token
    
    def to_dict(self):
        return {
            "email": self.email,
            "nome": self.nome,
            "token": self.token
        }
    
    @staticmethod
    def from_dict(data):
        if not data:
            return None
        return LoginDTO(
            email=data.get("email", ""),
            nome=data.get("nome", ""),
            token=data.get("token", "")
        )