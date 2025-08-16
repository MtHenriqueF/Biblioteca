# backend/app/schemas/editora.py
from pydantic import BaseModel
from typing import Optional

class EditoraBase(BaseModel):
    nome: str

class EditoraCreate(EditoraBase):
    pass

class Editora(EditoraBase):
    id_editora: int

    class Config:
        from_attributes = True

class EditoraUpdate(BaseModel):
    nome: Optional[str] = None