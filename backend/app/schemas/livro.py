from pydantic import BaseModel
from typing import Optional, List
from datetime import date

# Import schemas relacionados (ex: Editora, Autor)
from backend.app.schemas import editora as schemas_editora
from backend.app.schemas import autor as schemas_autor

class LivroBase(BaseModel):
    ISBN: str
    id_editora: int
    data_publicacao: date
    edicao: Optional[int] = None
    genero: Optional[str] = None
    titulo: str

class LivroCreate(LivroBase):
    autores_ids: Optional[List[int]] = None

class Livro(LivroBase):
    editora: schemas_editora.Editora
    autores: List[schemas_autor.Autor]

    class Config:
        from_attributes = True