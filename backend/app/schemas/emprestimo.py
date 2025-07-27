from pydantic import BaseModel
from typing import Optional
from datetime import date
from backend.app.schemas import exemplar as schemas_exemplar
from backend.app.schemas import usuario as schemas_usuario
from backend.app.schemas import funcionario as schemas_funcionario

class EmprestimoBase(BaseModel):
    id_exemplar: int
    id_usuario: int
    id_funcionario: int
    data_emprestimo: date
    data_devolucao_prev: Optional[date] = None
    data_devolucao: Optional[date] = None
    status: str

class EmprestimoCreate(EmprestimoBase):
    pass

class Emprestimo(EmprestimoBase):
    id_emprestimo: int
    exemplar: schemas_exemplar.Exemplar
    usuario: schemas_usuario.Usuario
    funcionario: schemas_funcionario.Funcionario

    class Config:
        from_attributes = True