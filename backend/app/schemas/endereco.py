from pydantic import BaseModel

class EnderecoBase(BaseModel):
    nome_bairro: str
    nome_rua: str

class EnderecoCreate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id_endereco: int

    class Config:
        from_attributes = True