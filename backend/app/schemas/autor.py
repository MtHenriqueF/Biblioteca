from pydantic import BaseModel
from typing import Optional

class AutorBase(BaseModel):
    nome: str
    nacionalidade: Optional[str] = None

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    id_autor: int

    class Config:
        from_attributes = True
