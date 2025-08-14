from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from decimal import Decimal
from backend.app.schemas import emprestimo as schemas_emprestimo

class PagamentoMultaBase(BaseModel):
    id_emprestimo: int
    valor_pago: Decimal = Field(..., gt=0, description="O valor pago deve ser maior que zero.") 

class PagamentoMultaCreate(PagamentoMultaBase):
    pass

class PagamentoMulta(PagamentoMultaBase):
    id_pagamento: int
    data_pagamento: Optional[date] = None
    # emprestimo: Optional[schemas_emprestimo.Emprestimo] = None
    emprestimo: schemas_emprestimo.Emprestimo


    class Config:
        from_attributes = True