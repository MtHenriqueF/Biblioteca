from pydantic import BaseModel
from typing import Optional
from backend.app.schemas import endereco as schemas_endereco

class FuncionarioBase(BaseModel):
    id_endereco: Optional[int] = None
    email: Optional[str] = None
    nome: Optional[str] = None
    cargo: Optional[str] = None

class FuncionarioCreate(FuncionarioBase):
    pass

class Funcionario(FuncionarioBase):
    id_funcionario: int
    endereco: Optional[schemas_endereco.Endereco] = None

    class Config:
        from_attributes = True

class FuncionarioUpdate(BaseModel):
    email: Optional[str] = None
    nome: Optional[str] = None
    cargo: Optional[str] = None
    id_endereco: Optional[int] = None