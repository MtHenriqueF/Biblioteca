# backend/app/schemas/editora.py
from pydantic import BaseModel

class EditoraBase(BaseModel):
    nome: str

class EditoraCreate(EditoraBase):
    pass

class Editora(EditoraBase):
    id_editora: int

    class Config:
        from_attributes = True