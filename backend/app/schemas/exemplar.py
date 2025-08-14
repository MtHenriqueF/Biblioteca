from pydantic import BaseModel
from typing import Optional
from backend.app.schemas import livro as schemas_livro

class ExemplarBase(BaseModel):
    ISBN: str
    status: str
    localizacao: Optional[str] = None

class ExemplarCreate(ExemplarBase):
    pass

class Exemplar(ExemplarBase):
    id_exemplar: int
    livro: schemas_livro.Livro

    class Config:
        from_attributes = True

class ExemplarUpdate(BaseModel):
    status: Optional[str] = None
    localizacao: Optional[str] = None