from pydantic import BaseModel
from typing import Optional
from backend.app.schemas import endereco as schemas_endereco

class UsuarioBase(BaseModel):
    id_endereco: Optional[int] = None
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id_usuario: int
    endereco: Optional[schemas_endereco.Endereco] = None

    class Config:
        from_attributes = True
    
class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    id_endereco: Optional[int] = None #Permite alterar o endereço do usuário
