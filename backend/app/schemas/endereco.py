from pydantic import BaseModel
from typing import Optional

class EnderecoBase(BaseModel):
    nome_bairro: str
    nome_rua: str

class EnderecoCreate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id_endereco: int

    class Config:
        from_attributes = True

class EnderecoUpdate(BaseModel):
    nome_bairro: Optional[str] = None
    nome_rua: Optional[str] = None
