import json
import os

from usuario_dto import UsuarioDTO
import usuario_dto

class UsuarioRepository:
    def __init__(self, caminho="data/usuarios.json"):
        self.caminho = caminho
        self._garantir_pasta()

    def _garantir_pasta(self):
        pasta = os.path.dirname(self.caminho)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    def _carregar(self):
        if not os.path.exists(self.caminho):
            return {}
        with open(self.caminho, "r", encoding="utf-8") as f:
            return json.load(f)
        return []
    
    def _salvar(self, dados):
        with open(self.caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2)

    def buscar_por_email(self, email):
        usuarios = self._carregar()
        for u in usuarios:
            if u.get("email") == email:
                return UsuarioDTO.from_dict(u)
        return None
    
    def salvar(self, usuario: usuario_dto):
        usuarios = self._carregar()
        for i, u in enumerate(usuarios):
            if u.get("email") == usuario.email:
                usuarios[i] = usuario.to_dict()
                self._salvar(usuarios)
                return True
        
        usuarios.append(usuario.to_dict())
        self._salvar(usuarios)
        return True
    
    def listar_todos(self):
        usuarios = self._carregar()
        return [UsuarioDTO.from_dict(u) for u in usuarios]
    
    
