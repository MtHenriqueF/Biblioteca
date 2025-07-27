from pydantic import BaseModel
from typing import Optional
from datetime import date
from backend.app.schemas import livro as schemas_livro
from backend.app.schemas import usuario as schemas_usuario
from backend.app.schemas import funcionario as schemas_funcionario

class ReservaBase(BaseModel):
    ISBN: str
    id_usuario: int
    id_funcionario: int
    data_reserva: Optional[date] = None # Deve ser definida automaticamente no backend
    status: Optional[str] = None

class ReservaCreate(ReservaBase):
    pass

class Reserva(ReservaBase):
    id_reserva: int
    livro: schemas_livro.Livro
    usuario: schemas_usuario.Usuario
    funcionario: schemas_funcionario.Funcionario

    class Config:
        from_attributes = True